# ascii_spotify
code for turning an ascii file into a Spotify playlist

## Installation
First you need to install pyspotify.  On OS X 10.9 I did:

`brew install homebrew/binary/libspotify`
`pip install --pre pyspotify`
(see [here](https://pyspotify.mopidy.com/en/latest/installation/) for details)

Then I went here https://developer.spotify.com/technologies/libspotify/keys/ to get the binary key.
(see [here](https://pyspotify.mopidy.com/en/latest/quickstart/#application-keys) for details).


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

You can mix and match those in a single file.
Note that we're leveraging the smart-search of capabilities of 
Spotify, so you can have some misspelling, use lower case, and 
drop some words.  Once it compiles all of the tracks, it will 
push those tracks into one or more new playlists in your Spotify 
account.  The new playlists will have names like 
[my_prefix0, my_prefix1, etc.].

Finally, if you want to add all of this music to "Your Music" on 
Spotify, click on a new playlist, select all the tracks, and drag to 
YourMusic/Songs.