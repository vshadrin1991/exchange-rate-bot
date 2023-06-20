from db_connector import DBConnector
from sqlalchemy import text


class Select(DBConnector):
    def select(self):
        return self.connection.execute(text("select * from users"))
