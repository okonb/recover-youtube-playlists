from argparse import ArgumentParser


def get_argument_parser() -> ArgumentParser:
    argument_parser = ArgumentParser(
        description="Recover YouTube playlists from the saved review website!\
                     Download the content takedown website and extract the\
                     playlist from it.\
                     Documentation and further development at\
                     https://github.com/okonb/recover-youtube-playlists",
        epilog="Copyright (c) 2023 Bartosz Okoń"
        )
    argument_parser.add_argument("filename",
                                 help="HTML file to be processed")
    argument_parser.add_argument("-v", "--verbose", action="store_true",
                                 help="display additional info")
    argument_parser.add_argument("--extra-info", action="store_true",
                                 help="store extra information available in the file")
    argument_parser.add_argument("-f", "--format", choices=["csv", "json"], default="csv",
                                 help="choose output format")
    argument_parser.add_argument("-e", "--extractor", choices=["auto", "v1"],
                                 default="auto", help="choose extractor version")
    return argument_parser
