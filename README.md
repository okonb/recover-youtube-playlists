# Recover YouTube playlists

Has YouTube unrightfully removed your beloved playlist you've been curating for the past 10 years?
Don't worry, you will most likely be able to recover it!

## READ THIS pretty please

This project aims to provide a way to extract and save a list of videos from your removed playlist. It can do this because YouTube shows you all the videos from a removed playlist in the content review website.

What you get at the end is a human- and computer-readable file containing titles, links (and more) of videos on your playlist. For example, you can open the resulting csv file in Google Spreadsheets and it will even let you click links!

The goal of this project though is not uploading the recovered playlist back to your YouTube account. I can't recommend doing so as this might trigger YouTube's deletion evasion detection and get you in even more trouble...

However if you were to risk it, you have two choices:
- paid but convenient service (like soundiiz or tunemymusic, both unchecked by me)
- uploading using someone else's project (cumbersome, requires a Google cloud app and shuffling passcodes)

This software is provided under the MIT license and the author does not guarantee it works correctly. [Full license](LICENSE)

Now after you've read the important stuff, you can move on to recovering your playlist by following the [✨instructions✨](docs/instructions.md).

The FAQ is [here](docs/FAQ.md).

## Usage
### Requirements
Python 3 (works with Python 3.10.12) and pip3 are required.

After cloning, execute `make` or `pip3 install -r requirements.txt`
.
### Running 
```
python3 recover_playlist.py filename  [-h]
                                      [--format {csv,excel-csv,json}]
                                      [--extractor {auto,v1}]
                                      [-o OUTPUT_FILENAME]
                                      [--extra-info]
                                      [--just-links]
                                      [--ids-only]
                                      [--no-lxml]
                                      [--log {DEBUG,INFO,WARNING,ERRORCRITICAL}]

positional arguments:
  filename              HTML file to be processed

options:
  -h, --help            show this help message and exit
  --format {csv,excel-csv,json}
                        choose output format (default: csv)
  --extractor {auto,v1}
                        choose extractor version (default: auto)
  -o OUTPUT_FILENAME, --output-filename OUTPUT_FILENAME
                        output file name (default: None)
  --extra-info          store extra information available in the file (default: False)
  --just_links          only export links to videos (may be needed for some services) (default: False)
  --ids_only            store links as video ids (default: False)
  --no-lxml             don't use lxml (default: False)
  --log {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        choose logging level (default: CRITICAL)
```

## Technical stuff

This project is just an overengineered version of what could have been two-pages worth of Python; and I'm sure there are better ways to write most of what I've used.

What we gain from all this though is easy extendability. YouTube updated their interface and the extractor no longer works? Write a new one, add it to the factory and you're set.

There is currently no testing because I don't think it makes sense to test for something as ephemeral as website scraping. Providing test files is also difficult when you only ever had one of your playlists removed AND poses some privacy concerns. :) This may change if the project grows beyond something quick and dirty.

## Contributing (?)

Issues and pull requests are very welcome, it would be awesome if this project could help people for as long as possible! Just please don't mind waiting a bit for a response, I can't guarantee that I'll always be available. :)