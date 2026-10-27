from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import pandas as pd

class DatabaseAdapter(ABC):
    """
    Abstract Database Adapter defining standard data access and analytical
    query capabilities for SignalFire AI across Exasol and local fallback engines.
    """

    @property
    @abstractmethod
    def backend_name(self) -> str:
        """Human-readable backend name (e.g. 'Exasol Personal' or 'DuckDB Local')."""
        pass

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """Current connectivity status."""
        pass

    @abstractmethod
    def connect(self) -> bool:
        """Establish or verify database connection."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Close connection if open."""
        pass

    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """Perform a live health check and latency measurement."""
        pass

    @abstractmethod
    def execute_query(self, sql: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Execute a query and return results as list of dictionaries."""
        pass

    @abstractmethod
    def execute_df(self, sql: str, params: Optional[Dict[str, Any]] = None) -> pd.DataFrame:
        """Execute query and return a pandas DataFrame."""
        pass

    @abstractmethod
    def execute_statement(self, sql: str, params: Optional[Dict[str, Any]] = None) -> int:
        """Execute a DDL or DML statement and return affected rows."""
        pass

    @abstractmethod
    def load_table(self, table_name: str, df: pd.DataFrame, if_exists: str = "replace") -> int:
        """Ingest a DataFrame into a target table."""
        pass

    @abstractmethod
    def list_tables(self) -> List[str]:
        """List all analytical tables currently available."""
        pass

    @abstractmethod
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Return schema details (column names, types, nullability)."""
        pass
