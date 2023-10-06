#!/usr/bin/python3
import os
from argparse import Namespace
from typing import Tuple, List
from datetime import datetime
from bs4 import BeautifulSoup
from util.Extractor import Extractor
from util.argument_parser import get_argument_parser
from util.extractor_factory import extractor_factory, extractor_version_map
from util.file_writers import write_json, write_csv


def main():

    args: Namespace = get_argument_parser().parse_args()
    to_parse: str = args.filename
    # verbose: bool = args.verbose
    extra_info: bool = args.extra_info
    extractor_version: str = args.extractor
    output_format: str = args.format

    print(f"Parsing file: {to_parse}...")
    try:
        with open(to_parse, 'r') as file:
            soup: BeautifulSoup = BeautifulSoup(file, features="lxml")
    except FileNotFoundError as e:
        print(e)
        exit(1)

    file_date_created: float = os.path.getctime(to_parse)

    extractor: Extractor

    if extractor_version == "auto":
        extractor = extractor_factory(file_date_created, extra_info)
    else:
        extractor = extractor_version_map[extractor_version](args.extra_info)

    print(f"Extracting using {extractor.version_str()} extractor...")

    playlist_title: str
    videos_list: List[Tuple]

    playlist_title, videos_list = extractor.process(soup)

    header_tuple: Tuple[str, ...] = extractor.get_header_tuple()

    outfile_name: str = playlist_title + "-" + \
        datetime.now().isoformat(timespec="seconds") + "." + output_format

    print(f"Saving to {outfile_name} using {output_format} writer...")
    with open(outfile_name, 'w', newline='') as file:
        match output_format:
            case "csv":
                write_csv(file, header_tuple, videos_list)
            case "json":
                write_json(file, header_tuple, videos_list)

    print(f"Successfully extracted {len(videos_list)} videos! Exiting.")


if __name__ == "__main__":
    main()
