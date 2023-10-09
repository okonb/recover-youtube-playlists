from abc import ABC, abstractmethod
from typing import Tuple, List
from bs4 import BeautifulSoup


class Extractor(ABC):
    @abstractmethod
    def get_header_tuple(self) -> Tuple[str, ...]:
        pass

    @abstractmethod
    def get_video_list(self, soup: BeautifulSoup) -> List[Tuple[str, ...]]:
        pass

    @abstractmethod
    def get_playlist_info(self, soup: BeautifulSoup) -> dict:
        pass

    @classmethod
    @abstractmethod
    def version_str(cls) -> str:
        pass
