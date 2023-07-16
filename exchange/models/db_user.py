from sqlalchemy import String, insert, select
from sqlalchemy.orm import Mapped, mapped_column

from exchange.entities import User
from exchange.logger import Log

from .base import Base
from .db_connector import DBConnector


class DBUser(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    def __init__(self, connector: DBConnector):
        self._connector: DBConnector = connector
        self.metadata.create_all(self._connector.engine)

    def __repr__(self) -> str:
        return f'user_id={self.user_id}, first_name={self.first_name}, last_name={self.last_name}'

    def insert(self, user: User):
        if (
            len(
                self._connector.connection.execute(
                    select('*')
                    .select_from(self.__class__)
                    .where(self.__class__.user_id == user.user_id)
                ).fetchall()
            )
            == 0
        ):
            self._connector.connection.execute(
                insert(self.__class__).values(
                    {
                        self.__class__.user_id: user.user_id,
                        self.__class__.first_name: user.first_name,
                        self.__class__.last_name: user.last_name,
                    }
                )
            ).connection.commit()
        else:
            Log.info(f'User {user.user_id} allready exist.')
