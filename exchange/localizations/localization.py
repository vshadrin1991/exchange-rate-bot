import json
import os
from pathlib import Path

from exchange.meta import SingletoneMeta


class Localization(metaclass=SingletoneMeta):
    def __init__(self, localization=os.getenv('LOCALIZATION')) -> None:
        self._local: dict = self.__read_local(localization)

    @property
    def local(self) -> dict:
        return self._local

    def __read_local(self, localization: str) -> dict:
        file_path: Path = Path('localizations', f'{localization.lower()}.json')
        return json.loads(file_path.read_text())
