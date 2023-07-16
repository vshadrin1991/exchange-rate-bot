from dataclasses import dataclass


@dataclass
class User:
    user_id: int
    first_name: str
    last_name: str
    message: str
    date: int
    chat_id: int
