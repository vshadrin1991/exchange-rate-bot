from sqlalchemy import String, insert, select
from sqlalchemy.orm import Mapped, mapped_column

from ..entities import User
from .base import Base
from .db_connector import DBConnector


class DBUserLog(Base):
    __tablename__ = 'user_log'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    html_text: Mapped[str] = mapped_column(String(245))
    date: Mapped[int]

    def __init__(self):
        self.metadata.create_all(DBConnector().engine)

    def __repr__(self) -> str:
        return f'user_id={self.user_id}, html_text={self.html_text}, date={self.date}'

    def insert(self, user: User):
        DBConnector().get_connection().execute(
            insert(self.__class__).values(
                {
                    self.__class__.user_id: user.user_id,
                    self.__class__.html_text: user.html_text,
                    self.__class__.date: user.date,
                }
            )
        ).connection.commit()

    def select_all(self) -> tuple:
        return (
            DBConnector()
            .get_connection()
            .execute(select('*').select_from(self.__class__))
            .fetchall()
        )
