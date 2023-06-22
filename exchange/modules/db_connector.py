from sqlalchemy import Engine, create_engine

from ..configs import config
from ..logger import Log
from ..meta import SingletoneMeta


class DBConnector(metaclass=SingletoneMeta):
    def __init__(self, db_url: str = config.DB_URL) -> None:
        self._engine = create_engine(url=db_url, echo=True)

    @property
    def engine(self) -> Engine:
        return self._engine

    def get_connection(self):
        try:
            Log.info('Try to connect to data base')
            conndection = self._engine.connect()
        except RuntimeError:
            raise RuntimeError(f'Opps... DB connection error to {config.DB_URL}')
        else:
            Log.info('Successfully DB connection')
            return conndection
