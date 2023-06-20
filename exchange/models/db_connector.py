from configs import config
from db_connector_meta import DBConnectorMeta
from sqlalchemy import create_engine


class DBConnector(metaclass=DBConnectorMeta):
    def __init__(self) -> None:
        self._engine = create_engine(url=config.DB_URL)
        self._connection = self._engine.connect()

    @property
    def connection(self):
        return self._connection
