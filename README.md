# ascii_spotify
Here's a bit of python code for generating a Spotify playlist from an ascii file.  Maybe you have a stack of records/tapes/CDs and want to get that music linked with your Spotify account.  Make a big ascii/txt file that looks like this inside:

```
george harrison, all things must pass
sonic youth
the smiths, all 
```
and this code will, after a bit of user authentification, add these tracks to a new Spotify playlist.  In this case, you'd get all the tracks on George Harrison's "All Things Must Pass", the "Top Hits" tracks of Sonic Youth (as determined by Spotify), and *all* the tracks from The Smiths.

## Installation
First you need to install pyspotify ([details here](https://pyspotify.mopidy.com/en/latest/installation/)).  On OS X 10.9 I did:

`brew install homebrew/binary/libspotify`

then

`pip install --pre pyspotify`

Then you need to get your [binary developer key](https://pyspotify.mopidy.com/en/latest/quickstart/#application-keys) from Spotify.  I got mine [here](https://developer.spotify.com/technologies/libspotify/keys/).


## Usage
Run as:
`python ascii_spotify.py my_playlist.txt my_prefix`

That will use the ascii file 'my_playlist.txt' to grab 
a bunch of tracks from Spotify.  There are three patterns for the lines
of this file

1. "ARTIST, ALBUM"
e.g. "george harrison, all things must pass"
which gets all the tracks from this album,

2. "ARTIST"
e.g. "the books"
which gets the Spotify "top hit" tracks by this artist, and

3. "ARTIST, ALL"
e.g. "fiery furnaces, all"
which gets every track by this artist.

You can mix and match those patterns in a single file.
Note that we're leveraging the smart-search of capabilities of 
Spotify, so you can have some misspelling, use lower case, and 
drop some words.  Once it compiles all of the tracks, it will 
push those tracks into one or more new playlists in your Spotify 
account.  The new playlists will have names like 
[my_prefix0, my_prefix1, etc.].  There are multiple playlists because
each one can hold at most 500 songs.

Finally, if you want to add all of this music to "Your Music" on 
Spotify, open the desktop Spotify program, click on a new 
playlist, select all the tracks, and drag to YourMusic/Songs.
