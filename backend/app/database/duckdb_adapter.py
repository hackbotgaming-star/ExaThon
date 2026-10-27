import time
import os
from typing import Any, Dict, List, Optional
import duckdb
import pandas as pd
from .base import DatabaseAdapter

class DuckDBAdapter(DatabaseAdapter):
    """
    Local analytical database adapter powered by DuckDB.
    Provides full SQL analytical capabilities for local development, demo mode,
    and automated testing when Exasol Personal is not configured or offline.
    """

    def __init__(self, db_path: Optional[str] = None):
        self._db_path = db_path or ":memory:"
        self._conn: Optional[duckdb.DuckDBPyConnection] = None
        self._connected = False
        self.connect()

    @property
    def backend_name(self) -> str:
        return "DuckDB Local (In-Process OLAP Engine)"

    @property
    def is_connected(self) -> bool:
        return self._connected and self._conn is not None

    def connect(self) -> bool:
        try:
            if self._conn is None:
                # If db_path is a file, ensure parent directory exists
                if self._db_path != ":memory:":
                    os.makedirs(os.path.dirname(os.path.abspath(self._db_path)), exist_ok=True)
                self._conn = duckdb.connect(database=self._db_path, read_only=False)
                self._connected = True
            return True
        except Exception as e:
            self._connected = False
            return False

    def disconnect(self) -> None:
        if self._conn is not None:
            try:
                self._conn.close()
            except Exception:
                pass
            self._conn = None
            self._connected = False

    def health_check(self) -> Dict[str, Any]:
        start = time.perf_counter()
        try:
            if not self.is_connected:
                self.connect()
            self._conn.execute("SELECT 1 AS ping").fetchall()
            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            return {
                "status": "healthy",
                "backend": self.backend_name,
                "latency_ms": latency_ms,
                "database": self._db_path,
                "connected": True,
                "message": "Local analytical engine operational."
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "backend": self.backend_name,
                "latency_ms": None,
                "database": self._db_path,
                "connected": False,
                "error": str(e)
            }

    def execute_query(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if not self.is_connected:
            self.connect()
        try:
            df = self.execute_df(sql, params)
            return df.to_dict(orient="records")
        except Exception as e:
            raise RuntimeError(f"DuckDB Query Error: {e}\nSQL: {sql}")

    def execute_df(self, sql: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        if not self.is_connected:
            self.connect()
        try:
            if params:
                return self._conn.execute(sql, params).df()
            return self._conn.execute(sql).df()
        except Exception as e:
            raise RuntimeError(f"DuckDB DataFrame Query Error: {e}\nSQL: {sql}")

    def execute_statement(self, sql: str, params: Optional[Dict[str, Any]] = None) -> int:
        if not self.is_connected:
            self.connect()
        try:
            if params:
                res = self._conn.execute(sql, params)
            else:
                res = self._conn.execute(sql)
            return 1
        except Exception as e:
            raise RuntimeError(f"DuckDB Statement Error: {e}\nSQL: {sql}")

    def load_table(self, table_name: str, df: pd.DataFrame, if_exists: str = "replace") -> int:
        if not self.is_connected:
            self.connect()
        try:
            # Register DataFrame and create or insert into table
            self._conn.register("temp_df_view", df)
            if if_exists == "replace":
                self._conn.execute(f"DROP TABLE IF EXISTS {table_name}")
                self._conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM temp_df_view")
            else:
                self._conn.execute(f"INSERT INTO {table_name} SELECT * FROM temp_df_view")
            self._conn.unregister("temp_df_view")
            return len(df)
        except Exception as e:
            raise RuntimeError(f"Failed to load table '{table_name}': {e}")

    def list_tables(self) -> List[str]:
        if not self.is_connected:
            self.connect()
        try:
            tables = self._conn.execute("SHOW TABLES").fetchall()
            return [t[0] for t in tables if not t[0].startswith("temp_")]
        except Exception:
            return []

    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        if not self.is_connected:
            self.connect()
        try:
            res = self._conn.execute(f"DESCRIBE {table_name}").fetchall()
            return [
                {
                    "column_name": row[0],
                    "column_type": str(row[1]),
                    "is_nullable": bool(row[2] == "YES") if len(row) > 2 else True,
                    "default_value": row[4] if len(row) > 4 else None
                }
                for row in res
            ]
        except Exception as e:
            raise RuntimeError(f"Could not describe table {table_name}: {e}")
