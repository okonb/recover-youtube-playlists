from io import TextIOWrapper
from typing import Tuple, List
import csv
import json


def write_csv(file: TextIOWrapper, header_tuple: Tuple[str, ...],
              videos_list: List[Tuple]):
    writer = csv.writer(file)
    writer.writerow(header_tuple)
    writer.writerows(videos_list)


def write_json(file: TextIOWrapper, header_tuple: Tuple[str, ...],
              videos_list: List[Tuple]):
    result = [dict(zip(header_tuple, video)) for video in videos_list]
    json.dump(result, file)
