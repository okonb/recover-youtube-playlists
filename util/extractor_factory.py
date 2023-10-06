from datetime import datetime
from time import mktime
from .Extractor import Extractor
from .VeeOneExtractor import VeeOneExtractor

extractor_version_map: dict = {"v1": VeeOneExtractor}


def extractor_factory(file_time_created: float, extra_info: bool) -> Extractor:
    if file_time_created < mktime(datetime(day=17, month=1, year=2038).timetuple()):
        return extractor_version_map["v1"](extra_info)
    raise Exception("hopefully unreachable")
