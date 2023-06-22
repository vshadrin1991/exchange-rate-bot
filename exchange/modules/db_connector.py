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
            conndection = self._engine.connect()
        except:
            Log.error('Opps... DB connection error')
        else:
            return conndection
