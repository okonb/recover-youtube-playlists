#!/usr/bin/python3
import os
import sys
import logging
from argparse import Namespace
from typing import Tuple, List
from datetime import datetime
from sanitize_filename import sanitize as fn_sanitize
from bs4 import BeautifulSoup
from util.extractor import Extractor
from util.argument_parser import get_argument_parser
from util.extractor_factory import extractor_factory, extractor_version_map
from util.file_writers import write_csv, write_excel_csv, write_json


def main():

    args: Namespace = get_argument_parser().parse_args()
    to_parse: str = args.filename
    extra_info: bool = args.extra_info
    extractor_version: str = args.extractor
    output_format: str = args.format
    just_links: bool = args.just_links
    ids_only: bool = args.ids_only
    log: str = args.log
    given_outfilename: str | None = args.output_filename

    loglevel = getattr(logging, log.upper())
    logging.basicConfig(filename="last.log", encoding='utf-8', level=loglevel,
                        filemode='w')

    if just_links:
        logging.debug("just links mode")
        extra_info = False

    if ids_only:
        logging.debug("id only mode")

    if given_outfilename is not None and \
            given_outfilename != fn_sanitize(given_outfilename):

        print("Provided output file name is not of correct format, exiting.")
        logging.critical("provided output filename %s not correct",
                         given_outfilename)
        sys.exit(1)

    print(f"Parsing file: {to_parse}...")
    logging.info("parsing %s", to_parse)

    try:
        with open(to_parse, 'r', encoding='utf-8') as file:
            soup: BeautifulSoup = BeautifulSoup(file, features="lxml")
    except FileNotFoundError as e:
        logging.critical("File %s not found; %s", to_parse, e)
        print(e)
        sys.exit(1)
    except Exception as e:
        logging.critical("couldn't parse html; %s", e)
        print("Couldn't parse the HTML file, exiting.")
        sys.exit(1)

    file_date_created: float = os.path.getctime(to_parse)

    extractor: Extractor

    if extractor_version == "auto":
        extractor = extractor_factory(file_date_created, extra_info, ids_only)
    else:
        extractor = extractor_version_map[extractor_version](args.extra_info)

    print(f"Extracting using {extractor.version_str()} extractor...")
    logging.info("using %s extractor, setting %s, file date %s",
                 extractor.version_str(), extractor_version,
                 datetime.fromtimestamp(file_date_created))

    playlist_title: str
    videos_list: List[Tuple[str, ...]]

    playlist_title, videos_list = extractor.process(soup)

    header_tuple: Tuple[str, ...] = extractor.get_header_tuple()

    if just_links:
        videos_list = [(vid[1],) for vid in videos_list]
        header_tuple = ("URL",)

    logging.info("extracted data. playlist title %s, header tuple %s",
                 playlist_title, header_tuple)

    file_extension: str = output_format if output_format != "excel-csv" \
        else "csv"

    outfile_name: str
    if given_outfilename is not None:
        outfile_name = given_outfilename
    else:
        outfile_name = playlist_title + "-" + \
            datetime.now().isoformat(timespec="seconds").replace(':', '-') + \
            "." + file_extension
        outfile_name = fn_sanitize(outfile_name)

    print(f"Saving to {outfile_name} using {output_format} writer...")
    logging.info("writing to %s, selected format %s",
                 outfile_name, output_format)
    try:
        with open(outfile_name, 'w', encoding='utf-8', newline='') as file:
            # a match would be cooler but i changed it for compatibility
            if output_format == "csv":
                write_csv(file, header_tuple, videos_list)
            elif output_format == "excel-csv":
                write_excel_csv(file, header_tuple, videos_list)
            elif output_format == "json":
                write_json(file, header_tuple, videos_list)
            else:
                raise Exception(f"Chosen file format {output_format} unknown.")
    except IOError as e:
        print("Couldn't save the playlist file, exiting.")
        logging.exception("can't write to %s; exception: %s", outfile_name, e)
        sys.exit(1)
    except Exception as e:
        print("Couldn't save the playlist file, exiting.")
        logging.exception("some error writing file: %s; %s",
                          sys.exc_info()[0], e)

    print(f"Successfully extracted {len(videos_list)} videos! Exiting.")
    logging.info("success extracting %d videos", len(videos_list))


if __name__ == "__main__":
    main()
