from dataclasses import dataclass


@dataclass
class User:
    user_id : int
    first_name : str
    last_name : str
    html_text : str
    date : int
