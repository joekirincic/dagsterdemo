
from dagster import ConfigurableResource, EnvVar
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine


class NYCFlights23(ConfigurableResource):
    host: str
    port: int
    database: str
    user: str
    password: str

    def _get_engine(self):
        """Create SQLAlchemy engine with current config."""
        connection_string = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        return create_engine(connection_string)
    
    @contextmanager
    def get_connection(self) -> Generator:
        """
        Context manager for database connections.
        Ensures connections are properly closed after use.
        
        Usage:
            with postgres_io_manager.get_connection() as conn:
                result = conn.execute(text("SELECT * FROM my_table"))
        
        Yields:
            SQLAlchemy Connection object
        """
        engine = self._get_engine()
        connection = engine.connect()
        try:
            yield connection
        finally:
            connection.close()
            engine.dispose()

nycflights23_db = NYCFlights23(
    host = EnvVar("DB_HOST"),
    port = EnvVar("DB_PORT"),
    database = EnvVar("DB_NAME"),
    user = EnvVar("DB_USER"),
    password = EnvVar("DB_PASSWORD")
)