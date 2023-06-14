from dataclasses import dataclass


@dataclass
class ExratesRates:
    Cur_ID: int
    Date: str
    Cur_Abbreviation: str
    Cur_Scale: int
    Cur_Name: str
    Cur_OfficialRate: float
