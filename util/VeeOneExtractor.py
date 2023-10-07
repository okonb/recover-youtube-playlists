import logging
from typing import List, Tuple
from bs4 import BeautifulSoup, Tag
from .Extractor import Extractor


class VeeOneExtractor(Extractor):
    def __init__(self, extra_info: bool, id_only: bool) -> None:
        super().__init__()
        self.extra_info = extra_info
        self.id_only = id_only

    def get_header_tuple(self) -> Tuple[str, ...]:
        if self.extra_info:
            return ("Id", "Title", "Length", "URL", "Thumbnail file")
        return ("Title", "URL")

    def process(self, soup: BeautifulSoup) -> Tuple[str, List[Tuple]]:
        _first_vid_tag: Tag | None = soup.find("a", class_="video-link")
        if _first_vid_tag is None:
            logging.critical("no _first_vid_tag")
            raise Exception(f"HTML file format invalid, please refer to\n\t\
                            {'https://github.com/okonb/recover-youtube-playlists'}")

        videos_object: Tag | None = _first_vid_tag.parent
        if videos_object is None:
            logging.critical("no videos_object")
            raise Exception("First video has no parent (?)")

        playlist_title: str
        _playlist_title_tag: Tag | None = videos_object.find("div", class_="playlist-title")
        if _playlist_title_tag is None or len(_playlist_title_tag.contents) != 1:
            logging.warning("can't extract playlist title")
            playlist_title = "Unknown playlist"
        else:
            playlist_title = str(_playlist_title_tag.contents[0])

        videos_list: List[Tuple] = []

        for i, video in enumerate(videos_object.find_all("a", class_="video-link")):
            if video is None:
                logging.warning("skipping video %d (None)", i)
                continue
            _title_tag: Tag | None = video.find("div", class_="playlist-title")
            if _title_tag is None:
                logging.warning("skipping video %d (_title_tag = None)", i)
                continue
            _title_list: List[str] = _title_tag.contents
            title: str
            if len(_title_list) != 1:
                logging.warning("can't extract video %d title", i)
                title = "Unknown"
            else:
                title = _title_list[0]
            link = video["href"]
            if link is None:
                logging.warning("link on video %d is None", i)
            elif self.id_only:
                link = link[-11:]
            if self.extra_info:
                _length_tag: Tag | None = video.find("div", class_="label")
                video_length: str
                if _length_tag is not None and len(_length_tag.contents) == 1:
                    video_length = str(_length_tag.contents[0]).strip()
                else:
                    logging.warning("can't extract video %d length", i)
                    video_length = "Unknown"
                _index_tag: Tag | None = video.find("div", class_="video-index")
                video_index: str
                if _index_tag is not None and len(_index_tag.contents) == 1:
                    video_index = str(_index_tag.contents[0])
                else:
                    logging.warning("can't extract video %d index", i)
                    video_index = "Unknown"
                _img_tag: Tag | None = video.find("img")
                thumbnail_source: str
                if _img_tag is not None:
                    thumbnail_source = str(_img_tag["src"])
                else:
                    logging.warning("can't extract video %d thumbnail", i)
                    thumbnail_source = "Unknown"
                videos_list.append((video_index, title, video_length, link,
                                    thumbnail_source))
            else:
                videos_list.append((title, link))
        return (playlist_title, videos_list)

    @classmethod
    def version_str(cls) -> str:
        return "v1"
