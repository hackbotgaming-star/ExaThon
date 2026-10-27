import os
import time
from typing import Any, Dict, List, Optional
import pandas as pd
from .base import DatabaseAdapter

class ExasolAdapter(DatabaseAdapter):
    """
    Exasol Personal database adapter using the official pyexasol driver.
    Connects to Exasol instances via WebSocket/JSON RPC protocol.
    Provides schema management, fast analytics queries, and ingestion.
    """

    def __init__(
        self,
        dsn: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        schema: Optional[str] = None,
        connection_timeout: int = 5
    ):
        self.dsn = dsn or os.getenv("EXASOL_DSN", "localhost:8563")
        self.user = user or os.getenv("EXASOL_USER", "sys")
        self.password = password or os.getenv("EXASOL_PASSWORD", "exasol")
        self.schema = schema or os.getenv("EXASOL_SCHEMA", "SIGNALFIRE")
        self.timeout = connection_timeout
        self._conn = None
        self._last_error: Optional[str] = None

    @property
    def backend_name(self) -> str:
        return "Exasol Personal (High-Performance In-Memory Analytics)"

    @property
    def is_connected(self) -> bool:
        if self._conn is None:
            return False
        try:
            # Check if internal websocket is still open
            return not self._conn.is_closed
        except Exception:
            return False

    def connect(self) -> bool:
        try:
            import pyexasol
            self._conn = pyexasol.connect(
                dsn=self.dsn,
                user=self.user,
                password=self.password,
                schema=self.schema,
                connection_timeout=self.timeout,
                autocommit=True
            )
            self._last_error = None
            return True
        except ImportError:
            self._last_error = "pyexasol driver is not installed."
            self._conn = None
            return False
        except Exception as e:
            self._last_error = str(e)
            self._conn = None
            return False

    def disconnect(self) -> None:
        if self._conn is not None:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None

    def health_check(self) -> Dict[str, Any]:
        start = time.perf_counter()
        if not self.is_connected:
            connected = self.connect()
            if not connected:
                return {
                    "status": "disconnected",
                    "backend": self.backend_name,
                    "dsn": self.dsn,
                    "schema": self.schema,
                    "connected": False,
                    "latency_ms": None,
                    "error": self._last_error or "Could not connect to Exasol host",
                    "instructions": "Ensure Exasol Personal Docker or VM is running and EXASOL_DSN is reachable."
                }

        try:
            # Query Exasol version and time
            stmt = self._conn.execute("SELECT PARAM_VALUE FROM SYS.EXA_METADATA WHERE PARAM_NAME = 'databaseProductVersion'")
            row = stmt.fetchone()
            version = row[0] if row else "Exasol 7.x/8.x"
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            return {
                "status": "healthy",
                "backend": self.backend_name,
                "version": version,
                "dsn": self.dsn,
                "schema": self.schema,
                "connected": True,
                "latency_ms": latency_ms,
                "message": f"Connected to Exasol Personal ({version})"
            }
        except Exception as e:
            self._last_error = str(e)
            return {
                "status": "unhealthy",
                "backend": self.backend_name,
                "dsn": self.dsn,
                "connected": False,
                "latency_ms": None,
                "error": str(e)
            }

    def execute_query(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        df = self.execute_df(sql, params)
        return df.to_dict(orient="records")

    def execute_df(self, sql: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        if not self.is_connected and not self.connect():
            raise ConnectionError(f"Cannot execute query. Exasol not connected: {self._last_error}")
        try:
            return self._conn.export_to_pandas(sql, query_params=params)
        except Exception as e:
            # Fall back to standard fetch if export_to_pandas fails on specific DDL/metadata
            try:
                stmt = self._conn.execute(sql, query_params=params)
                columns = [col['name'] for col in stmt.columns()]
                rows = stmt.fetchall()
                return pd.DataFrame(rows, columns=columns)
            except Exception as inner_e:
                raise RuntimeError(f"Exasol Query Execution Failed: {inner_e}")

    def execute_statement(self, sql: str, params: Optional[Dict[str, Any]] = None) -> int:
        if not self.is_connected and not self.connect():
            raise ConnectionError(f"Cannot execute statement. Exasol not connected: {self._last_error}")
        try:
            stmt = self._conn.execute(sql, query_params=params)
            return stmt.rowcount() if hasattr(stmt, 'rowcount') else 1
        except Exception as e:
            raise RuntimeError(f"Exasol Statement Failed: {e}")

    def load_table(self, table_name: str, df: pd.DataFrame, if_exists: str = "replace") -> int:
        if not self.is_connected and not self.connect():
            raise ConnectionError(f"Cannot load table. Exasol not connected: {self._last_error}")
        try:
            if if_exists == "replace":
                self._conn.execute(f"DROP TABLE IF EXISTS {self.schema}.{table_name}")
            
            # Use pyexasol's fast import_from_pandas
            self._conn.import_from_pandas(df, (self.schema, table_name))
            return len(df)
        except Exception as e:
            raise RuntimeError(f"Failed to import DataFrame to Exasol table {table_name}: {e}")

    def list_tables(self) -> List[str]:
        if not self.is_connected and not self.connect():
            return []
        try:
            sql = f"SELECT TABLE_NAME FROM SYS.EXA_ALL_TABLES WHERE TABLE_SCHEMA = '{self.schema.upper()}'"
            res = self.execute_query(sql)
            return [r["TABLE_NAME"] for r in res]
        except Exception:
            return []

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        if not self.is_connected and not self.connect():
            return []
        try:
            sql = f"""
            SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_IS_NULLABLE, COLUMN_DEFAULT
            FROM SYS.EXA_ALL_COLUMNS
            WHERE TABLE_SCHEMA = '{self.schema.upper()}'
              AND TABLE_NAME = '{table_name.upper()}'
            ORDER BY COLUMN_ORDINAL_POSITION
            """
            rows = self.execute_query(sql)
            return [
                {
                    "column_name": r.get("COLUMN_NAME"),
                    "column_type": r.get("COLUMN_TYPE"),
                    "is_nullable": r.get("COLUMN_IS_NULLABLE") == "TRUE",
                    "default_value": r.get("COLUMN_DEFAULT")
                }
                for r in rows
            ]
        except Exception as e:
            raise RuntimeError(f"Could not describe Exasol table {table_name}: {e}")
