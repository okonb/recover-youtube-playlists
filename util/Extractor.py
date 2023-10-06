from abc import ABC, abstractmethod
from typing import Tuple, List
from bs4 import BeautifulSoup


class Extractor(ABC):
    @abstractmethod
    def get_header_tuple(self) -> Tuple[str, ...]:
        pass

    @abstractmethod
    def process(self, soup: BeautifulSoup) -> Tuple[str, List[Tuple]]:
        pass

    @classmethod
    @abstractmethod
    def version_str() -> str:
        pass
