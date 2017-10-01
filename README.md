# iTunes Artworker

iTunes Artworker is a python script that does a few things:

- Downloads album art for either a single specified album or your entire iTunes library
- Replaces either the single specified album artwork, or rebuilds entire iTunes library's album artwork

The script works with both MP3 and M4A (AAC) audo files! More compatability can be added although I haven't found the need.

### Assumptions

- You are using Mac OS as your operating system
- Your iTunes library is stored in /Users/YOURUSER/Music/iTunes

### Usage

To use iTunes Artworker clone this repo and:

- Change directories into the repo `cd iTunes-Artworker-master`
- Run `pip install -r requirements.txt`
- Run `python itunes.py`

The script ignores albums with the title "Unknown Album" simply because there is no album name, therefore no album artwork.

Album artwork is stored in a folder created called `/album_art` with each album artwork having its own folder.

Currently you have to re-import your music to iTunes after it has a new album artwork.

### To Do

- Check whether albums already have artwork, if so, skip them
- If album is called "Unknown Album", get song title(s) inside album and search for album name