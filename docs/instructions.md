# Instructions

### Step one - acquiting data
First you need to secure your data source. Search your email inbox for the message announcing playlist's removal (keywords: youtube, removed). Finding that email is really important, since as far as I know, it is the only way to get to this page (correct me if I'm wrong though). The exact phrasing of things to click may be slightly diffenent from what I write here since the email I've received wasn't in English, but it should be close enough. Click "More info". After waiting a while for the website to load, click "Review your content". Now you're able to see all the videos from your removed playlist. A great time to let out a sigh of relief.


Now, press ctrl+s or right-click somewhere and chose "Save". In the new window, choose a place to download into and for the filetype select "Webpage, complete". This is very important as other choices don't save the list of videos. For me, the download process took around 10 minutes (decent internet connection, almost 5000 videos).

### Step two - extracting the playlist

Make sure you have Python 3.9 (or later) installed.

After cloning the repository (or downloading zipped code and extracting it), execute the appropriate setup command.

If you're on Linux, execute `make` in the repository root folder.

If you're on Windows, execute this command:
```
pip3 install -r requirements.txt
```
If the above command gives you an error related to lxml, use the `--no-lxml` option at the end of the next command.

If `python3` and `pip3` don't seem to work for you, try `python` and `pip`.


Let's say you want an excel-friendly csv file with additional information like video duration. The command to run is:
```sh
python3 recover_playlist.py --extra-info --format excel-csv /path/to/my_file.html
```
After running for a couple seconds, this will produce a file named `playlist_name-<current_date_and_time>.csv` in the same directory.

Congrats, that's your recovered file! You can open it in a spreadsheet and browse your playlist, or try to put it back on YouTube (more info in the [README](../README.md)).

If the extraction doesn't succeed, add `--log DEBUG` at the end of your command and re-run it. Then take a look at the produced `last.log` file and try to figure out a reason why it's not working. If you can't, file an issue on the repository's webpage.

You can see more options for running the extraction after executing:
```sh
python3 recover_playlist.py --help
```