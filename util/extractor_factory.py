from datetime import datetime
from time import mktime
from .extractor import Extractor
from .vee_one_extractor import VeeOneExtractor

extractor_version_map: dict = {VeeOneExtractor.version_str(): VeeOneExtractor}


def extractor_factory(file_time_created: float, extra_info: bool, id_only: bool) -> Extractor:
    # this is meant to be extended when youtube changes its UI and
    # v1 extractor no longer works
    if file_time_created < mktime(datetime(day=17, month=1, year=2038).timetuple()):
        return extractor_version_map[VeeOneExtractor.version_str()](extra_info, id_only)
    raise RuntimeError("this script has expired, fix it")
