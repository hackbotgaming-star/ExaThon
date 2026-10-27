import os
from typing import Any, Dict, List, Optional
import pandas as pd
from .base import DatabaseAdapter
from .duckdb_adapter import DuckDBAdapter
from .exasol_adapter import ExasolAdapter

class DatabaseManager:
    """
    Central database manager orchestrating analytical database connections.
    Supports seamless switching between Exasol Personal and DuckDB Local fallback.
    Never misrepresents local calculations as Exasol-powered.
    """

    def __init__(self):
        self.duckdb_adapter = DuckDBAdapter(db_path=os.getenv("DUCKDB_PATH", "signalfire_local.duckdb"))
        self.exasol_adapter: Optional[ExasolAdapter] = None
        
        # Check if Exasol environment variables are supplied
        dsn = os.getenv("EXASOL_DSN")
        if dsn:
            self.exasol_adapter = ExasolAdapter(
                dsn=dsn,
                user=os.getenv("EXASOL_USER", "sys"),
                password=os.getenv("EXASOL_PASSWORD", ""),
                schema=os.getenv("EXASOL_SCHEMA", "SIGNALFIRE")
            )
            # Try connecting initially
            if self.exasol_adapter.connect():
                self._active_backend = "EXASOL"
            else:
                self._active_backend = "DUCKDB"
        else:
            self._active_backend = "DUCKDB"

    @property
    def active_mode(self) -> str:
        """Returns 'EXASOL' or 'DUCKDB'."""
        return self._active_backend

    @property
    def adapter(self) -> DatabaseAdapter:
        if self._active_backend == "EXASOL" and self.exasol_adapter and self.exasol_adapter.is_connected:
            return self.exasol_adapter
        return self.duckdb_adapter

    def get_status(self) -> Dict[str, Any]:
        """Provides transparency on which database engine is executing queries."""
        current_adapter = self.adapter
        hc = current_adapter.health_check()
        
        exasol_status = None
        if self.exasol_adapter:
            exasol_status = self.exasol_adapter.health_check()
        else:
            exasol_status = {
                "configured": False,
                "connected": False,
                "message": "EXASOL_DSN environment variable not set. Running in Local DuckDB Mode."
            }

        return {
            "active_mode": self._active_backend,
            "active_backend_name": current_adapter.backend_name,
            "is_exasol_active": self._active_backend == "EXASOL",
            "health": hc,
            "exasol_status": exasol_status,
            "available_backends": ["DUCKDB", "EXASOL"]
        }

    def switch_backend(self, mode: str, exasol_config: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        mode = mode.upper()
        if mode == "EXASOL":
            if exasol_config:
                self.exasol_adapter = ExasolAdapter(
                    dsn=exasol_config.get("dsn"),
                    user=exasol_config.get("user", "sys"),
                    password=exasol_config.get("password", ""),
                    schema=exasol_config.get("schema", "SIGNALFIRE"),
                    connection_timeout=exasol_config.get("timeout", 5)
                )
            elif not self.exasol_adapter:
                self.exasol_adapter = ExasolAdapter()

            connected = self.exasol_adapter.connect()
            if connected:
                self._active_backend = "EXASOL"
                return {"success": True, "message": "Successfully connected and switched to Exasol Personal.", "mode": "EXASOL"}
            else:
                return {
                    "success": False,
                    "message": f"Could not connect to Exasol: {self.exasol_adapter._last_error}. Remaining on DuckDB.",
                    "mode": self._active_backend
                }
        elif mode == "DUCKDB":
            self._active_backend = "DUCKDB"
            return {"success": True, "message": "Switched to DuckDB local analytical engine.", "mode": "DUCKDB"}
        else:
            return {"success": False, "message": f"Unknown mode: {mode}", "mode": self._active_backend}

    def execute_df(self, sql: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        return self.adapter.execute_df(sql, params)

    def execute_query(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return self.adapter.execute_query(sql, params)

    def execute_statement(self, sql: str, params: Optional[Dict[str, Any]] = None) -> int:
        return self.adapter.execute_statement(sql, params)

    def load_table(self, table_name: str, df: pd.DataFrame, if_exists: str = "replace") -> int:
        # Load into active adapter; if DuckDB is fallback, also ensure DuckDB has it
        count = self.adapter.load_table(table_name, df, if_exists)
        # If active is Exasol, also mirror to DuckDB local cache for fast offline fallback
        if self._active_backend == "EXASOL":
            try:
                self.duckdb_adapter.load_table(table_name, df, if_exists)
            except Exception:
                pass
        return count

    def list_tables(self) -> List[str]:
        return self.adapter.list_tables()

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        return self.adapter.get_table_schema(table_name)

# Global singleton
db_manager = DatabaseManager()
