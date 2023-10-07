#!/usr/bin/python3
import os
import sys
import logging
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
    just_links: bool = args.just_links
    id_only: bool = args.id_only
    log: str = args.log

    loglevel = getattr(logging, log.upper())
    logging.basicConfig(filename="last.log", encoding='utf-8', level=loglevel,
                        filemode='w')

    if just_links:
        logging.debug("just links mode")
        extra_info = False

    if id_only:
        logging.debug("id only mode")

    print(f"Parsing file: {to_parse}...")
    logging.info("parsing %s", to_parse)
    
    try:
        with open(to_parse, 'r') as file:
            soup: BeautifulSoup = BeautifulSoup(file, features="lxml")
    except FileNotFoundError as e:
        logging.critical("File %s not found; %s", to_parse, e)
        print(e)
        exit(1)
    except Exception as e:
        logging.critical("couldn't parse html; %s", e)
        print("Couldn't parse the HTML file, exiting.")
        exit(1)

    file_date_created: float = os.path.getctime(to_parse)

    extractor: Extractor

    if extractor_version == "auto":
        extractor = extractor_factory(file_date_created, extra_info, id_only)
    else:
        extractor = extractor_version_map[extractor_version](args.extra_info)

    print(f"Extracting using {extractor.version_str()} extractor...")
    logging.info("using %s extractor, setting %s, file date %s",
                 extractor.version_str(), extractor_version,
                 datetime.fromtimestamp(file_date_created))

    playlist_title: str
    videos_list: List[Tuple]

    playlist_title, videos_list = extractor.process(soup)

    header_tuple: Tuple[str, ...] = extractor.get_header_tuple()

    if just_links:
        videos_list = [(vid[1],) for vid in videos_list]
        header_tuple = ("URL",)

    logging.info("extracted data. playlist title %s, header tuple %s",
                 playlist_title, header_tuple)

    outfile_name: str = playlist_title + "-" + \
        datetime.now().isoformat(timespec="seconds") + "." + output_format

    print(f"Saving to {outfile_name} using {output_format} writer...")
    logging.info("writing to %s, selected format %s",
                 outfile_name, output_format)
    try:
        with open(outfile_name, 'w', encoding='utf-8', newline='') as file:
            match output_format:
                case "csv":
                    write_csv(file, header_tuple, videos_list)
                case "json":
                    write_json(file, header_tuple, videos_list)
    except IOError as e:
        print("Couldn't save the playlist file, exiting.")
        logging.exception("can't write to %s; exception: %s", outfile_name, e)
        exit(1)
    except Exception as e:
        print("Couldn't save the playlist file, exiting.")
        logging.exception("some error writing file: %s; %s",
                          sys.exc_info()[0], e)

    print(f"Successfully extracted {len(videos_list)} videos! Exiting.")
    logging.info("success extracting %d videos",len(videos_list) )


if __name__ == "__main__":
    main()
