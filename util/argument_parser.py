from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def get_argument_parser() -> ArgumentParser:
    argument_parser = ArgumentParser(
        description="Recover YouTube playlists from the saved review website!\
                     Download the content takedown website and extract your\
                     playlist from it.\
                     Documentation and further development at\
                     https://github.com/okonb/recover-youtube-playlists",
        epilog="Copyright (c) 2023 Bartosz Okoń",
        formatter_class=ArgumentDefaultsHelpFormatter)
    argument_parser.add_argument("filename",
                                 help="HTML file to be processed")
    argument_parser.add_argument("--format",
                                 choices=["csv", "excel-csv", "json"],
                                 default="csv", help="choose output format")
    argument_parser.add_argument("--extractor",
                                 choices=["auto", "v1"],
                                 default="auto",
                                 help="choose extractor version")
    argument_parser.add_argument("--extra-info", action="store_true",
                                 help="store extra information available in \
                                       the file")
    argument_parser.add_argument("--just_links", action="store_true",
                                 help="only export links\
                                 to videos (may be needed for some services)")
    argument_parser.add_argument("--id_only", action="store_true",
                                 help="store links as video ids")
    argument_parser.add_argument("--log",
                                 choices=["DEBUG", "INFO", "WARNING", "ERROR",
                                          "CRITICAL"],
                                 default="CRITICAL",
                                 help="choose logging level")
    return argument_parser
