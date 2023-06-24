from sqlalchemy import Connection, Engine, create_engine
from sqlalchemy.exc import OperationalError

from exchange.configs import config
from exchange.logger import Log
from exchange.meta import SingletoneMeta


class DBConnector(metaclass=SingletoneMeta):
    def __init__(self, db_url: str = config.DB_URL) -> None:
        self._engine: Engine = create_engine(url=db_url, echo=True)
        self._connection: Connection = self._get_connection()

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def connection(self) -> Connection:
        return self._connection

    def _get_connection(self) -> Connection:
        try:
            Log.info('connect to data base')
            connection: Connection = self.engine.connect()
        except OperationalError as err:
            Log.error(f'opps... DB connection error to {config.DB_URL}')
            raise err
        else:
            Log.info('successfully DB connection')
            return connection
