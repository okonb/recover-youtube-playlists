from abc import ABC, abstractmethod
from typing import Tuple, List, TypedDict
from bs4 import BeautifulSoup


class InfoDict(TypedDict):
    playlist_title: str

class Extractor(ABC):

    @abstractmethod
    def get_header_tuple(self) -> Tuple[str, ...]:
        pass

    @abstractmethod
    def get_video_list(self, soup: BeautifulSoup) -> List[Tuple[str, ...]]:
        pass

    @abstractmethod
    def get_playlist_info(self, soup: BeautifulSoup) -> InfoDict:
        pass

    @classmethod
    @abstractmethod
    def version_str(cls) -> str:
        pass
