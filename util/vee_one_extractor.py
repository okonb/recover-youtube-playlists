from __future__ import annotations
import logging
from typing import List, Tuple
from bs4 import BeautifulSoup, Tag, PageElement
from .extractor import Extractor, InfoDict


class VeeOneInfoDict(InfoDict):
    # playlist_title: str (inherited)
    playlist_description: str
    reported_length: str


class VeeOneExtractor(Extractor):
    def __init__(self, extra_info: bool, id_only: bool) -> None:
        super().__init__()
        self.extra_info = extra_info
        self.id_only = id_only

    def get_header_tuple(self) -> Tuple[str, ...]:
        if self.extra_info:
            return ("id", "title", "duration", "url", "thumbnail")
        return ("title", "url")

    def get_video_list(self, soup: BeautifulSoup) -> List[Tuple[str, ...]]:

        videos_object: Tag | None = self._get_videos_object(soup)
        if videos_object is None:
            logging.critical("no videos_object")
            raise RuntimeError("First video has no parent (?)")

        videos_list: List[Tuple[str, ...]] = []

        for i, video in enumerate(videos_object.find_all("a", class_="video-link")):
            if video is None:
                logging.warning("skipping video %d (None)", i)
                continue
            _title_tag: Tag | None = video.find("div", class_="playlist-title")
            if _title_tag is None:
                logging.warning("skipping video %d (_title_tag = None)", i)
                continue
            _title_list: List[PageElement] = _title_tag.contents
            title: str
            if len(_title_list) != 1:
                logging.warning("can't extract video %d title", i)
                title = "Unknown"
            else:
                title = str(_title_list[0]).strip()
            link = video["href"]
            if link is None:
                logging.warning("link on video %d is None", i)
            else:
                link = link.strip()
                if self.id_only:
                    link = link[-11:]
            if self.extra_info:
                _duration_tag: Tag | None = video.find("div", class_="label")
                video_duration: str
                if _duration_tag is not None and len(_duration_tag.contents) == 1:
                    video_duration = str(_duration_tag.contents[0]).strip()
                else:
                    logging.warning("can't extract video %d duration", i)
                    video_duration = "Unknown"
                _index_tag: Tag | None = video.find("div", class_="video-index")
                video_index: str
                if _index_tag is not None and len(_index_tag.contents) == 1:
                    video_index = str(_index_tag.contents[0]).strip()
                else:
                    logging.warning("can't extract video %d index", i)
                    video_index = "Unknown"
                _img_tag: Tag | None = video.find("img")
                thumbnail_source: str
                if _img_tag is not None:
                    thumbnail_source = str(_img_tag["src"]).strip()
                else:
                    logging.warning("can't extract video %d thumbnail", i)
                    thumbnail_source = "Unknown"
                videos_list.append((video_index, title, video_duration, link,
                                    thumbnail_source))
            else:
                videos_list.append((title, link))
        return videos_list

    def get_playlist_info(self, soup: BeautifulSoup) -> VeeOneInfoDict:
        videos_object: Tag | None = self._get_videos_object(soup)
        playlist_title: str
        _playlist_title_tag: Tag | None = videos_object.find("div", class_="playlist-title")  # type: ignore
        if _playlist_title_tag is None or len(_playlist_title_tag.contents) != 1:
            logging.warning("can't extract playlist title")
            playlist_title = "Unknown playlist"
        else:
            playlist_title = str(_playlist_title_tag.contents[0]).strip()

        _playlist_description_tag: Tag | None = videos_object.find("yt-formatted-string")  # type: ignore
        playlist_description: str
        if _playlist_description_tag is None or len(_playlist_description_tag.contents) != 1:
            logging.warning("can't extract playlist description")
            playlist_description = "Unknown playlist description"
        else:
            playlist_description = str(_playlist_description_tag.contents[0]).strip()

        _reported_length_tag: Tag | None = videos_object.find("span", class_="playlist-size")  # type: ignore
        reported_length: str
        if _reported_length_tag is None or len(_reported_length_tag.contents) != 1:
            logging.warning("can't extract playlist reported length")
            reported_length = "Unknown playlist reported length"
        else:
            reported_length = str(_reported_length_tag.contents[0]).strip()

        return {
            "playlist_title": playlist_title,
            "playlist_description": playlist_description,
            "reported_length": reported_length
        }

    @staticmethod
    def version_str() -> str:
        return "v1"

    @staticmethod
    def _get_videos_object(soup: BeautifulSoup) -> Tag | None:
        _first_vid_tag: Tag | None = soup.find("a", class_="video-link")  # type: ignore
        if _first_vid_tag is None:
            logging.critical("no _first_vid_tag")
            raise RuntimeError("HTML file format invalid, please refer to\n\t" +
                            "https://github.com/okonb/recover-youtube-playlists")
        return _first_vid_tag.parent
