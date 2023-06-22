from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .db_connector import DBConnector


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int]
    first_name: Mapped[str]
    last_name: Mapped[str]

    def __init__(self):
        self.metadata.create_all(DBConnector().engine)

    def __repr__(self) -> str:
        return f'user_id={self.user_id}, first_name={self.first_name}, last_name={self.last_name}'
