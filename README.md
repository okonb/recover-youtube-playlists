# Recover YouTube playlists

Has YouTube unrightfully removed your beloved playlist you've curated for the past 10 years?
Well then worry not, as you will most likely able to recover it!

## READ THIS pretty please

This project aims to provide a way to extract and save the list of videos from your removed playlist. It can do this because YouTube shows you all the videos from a removed playlist in the content review website.

What you get at the end is a human- and computer-readable file containing titles, links (and more) of videos on your playlist. For example, you can open the resulting csv file in Google Spreadsheets and it will even let you click the links!

The goal of this project though is not uploading the recovered playlist back to your YouTube account. I can't recommend doing so as this might trigger YouTube's deletion evasion detection and get you in even more trouble...

However if you were to risk it, you have two choices:
- paid but convenient service (like soundiiz or tunemymusic, both unchecked by me)
- uploading using someone else's project (cumbersome, requires a Google cloud app and shuffling passcodes)

This software is provided under the MIT license and the author does not guarantee it works correctly. [Full license](LICENSE)

Now after you've read the important stuff, you can move on to recovering your playlist by following the [✨instructions✨](docs/instructions.md).

## Usage
### Requirements
Python 3 and pip3 are required.

After cloning execute `make` or `pip3 install -r requirements.txt`
.
### Running 
```
python3 recover_playlist.py filename [-h] [--format {csv,excel-csv,json}] [--extractor {auto,v1}] [--extra-info] [--just_links] [--id_only] [--log {DEBUG,INFO,WARNING,ERRORCRITICAL}]

positional arguments:
  filename              HTML file to be processed

options:
  -h, --help            show this help message and exit
  --format {csv,excel-csv,json}
                        choose output format (default: csv)
  --extractor {auto,v1}
                        choose extractor version (default: auto)
  --extra-info          store extra information available in the file (default: False)
  --just_links          only export links to videos (may be needed for some services) (default: False)
  --id_only             store links as video ids (default: False)
  --log {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        choose logging level (default: CRITICAL)
```

