import spotify

'''
Run as:
python ascii_spotify.py my_playlist.txt my_prefix

That will use the ascii file 'my_playlist.txt' to grab 
a bunch of tracks from Spotify.  There are three patterns for the lines
of this file

1) ARTIST, ALBUM
e.g. "george harrison, all things must pass"
which gets all the tracks from this album,

2) ARTIST
e.g. "the books"
which gets the Spotify "top hit" tracks by this artist, and

3) ARTIST, ALL
e.g. "fiery furnaces, all"
which gets every track by this artist.

Note that we're leveraging the smart-search of capabilities of 
Spotify, so you can have some misspelling, use lower case, and 
drop some words.  Once it compiles all of the tracks, it will 
push those tracks into one or more new playlists in your Spotify 
account.  The new playlists will have names like 
[my_prefix0, my_prefix1, etc.].  There are multiple playlists 
because each one can hold at most 500 songs.

Finally, if you want to add all of this music to "Your Music" on 
Spotify, open the desktop Spotify program, click on a new 
playlist, select all the tracks, and drag to YourMusic/Songs.
'''

def main():
    from sys import argv
    if len(argv)==1:
        ascii_filename = 'playlist.txt'
        new_playlist_prefix = 'ascii'
    if len(argv)==2:
        ascii_filename = argv[1]
        new_playlist_prefix = 'ascii'
    elif len(argv)==3:
        ascii_filename = argv[1]
        new_playlist_prefix = argv[2]
    ascii = AsciiUploader()
    ascii.get_tracks_from_ascii(ascii_filename)
    ascii.add_tracks_to_playlists(new_playlist_prefix)


class AsciiUploader():

    def __init__(self):
        self.load_session()
        self.event_loop = spotify.EventLoop(self.session)
        self.event_loop.start()
        
    def __del__(self):
        self.event_loop.stop()

    def load_session(self):
        from time import sleep
        import getpass
        session = spotify.Session()
        username = raw_input('spotify username: ')
        password = getpass.getpass('password: ')
        session.login(username, password)
        counter=0
        while (session.connection.state.real!=1):
            print '.'
            session.process_events()
            sleep(0.2)
            counter += 1
            if (counter>50):
                print 'Could not authenticate session!'
                #tmpp, need to handle this better.
                self.session = False
                break
        print '--- spotify session authenticated ---'
        self.session = session

    def get_tracks_from_ascii(self, ascii_name):
        f = open(ascii_name,'r')
        tracks = []
        for line in f:
            if len(line.rsplit())==0: continue
            # get artist/album info
            artist, album = self.artist_album_from_line(line)
            # get the tracks to add.
            tracks = (tracks + 
                      self.get_tracks_from_artist_and_album(artist, album))
        self.tracks = tracks
        self.viz_tracks_to_add()

    def artist_album_from_line(self, line):
        tmp = line.split(',')
        if len(tmp)==1:
            artist = tmp[0].rstrip()
            album = ''
        elif len(tmp)==2:
            artist = tmp[0].rstrip().strip()
            album = tmp[1].rstrip().strip()
        return artist, album

    def get_tracks_from_artist_and_album(self, artist_search_string, 
                                         album_search_string):
        search = self.session.search(
            artist_search_string, 
            search_type=spotify.SearchType.SUGGEST).load()
        if search.artist_total==0: return []
        # take only first artist.
        artist = search.artists[0]
        print ' '
        print 'ARTIST: searched "%s", got "%s"' % (
            artist_search_string.encode('utf-8'), 
            artist.name.encode('utf-8'))
        artist_browser = artist.browse().load()
        if len(artist_browser.albums)==0: return []
        if type(album_search_string)!=str: return []

        # process this album.
        print 'album string is %s'%(album_search_string)
        if album_search_string=='':
            tracks = self.get_tophit_tracks_from_artist(artist_browser)
        elif album_search_string.lower()=='all':
            tracks = self.get_all_tracks_from_artist(artist_browser)
        else:
            tracks = self.get_tracks_from_one_album(album_search_string, 
                                                    artist_browser)
        return tracks

    def get_tophit_tracks_from_artist(self, artist_browser):
        print 'getting "top hit" tracks.'
        tophit = artist_browser.tophit_tracks
        if len(tophit)==0:
            artist_name = artist_browser.artist.name
            print '*** NO TOP HIT TRACKS for %s ***'%(artist_name)
            return []
        return list(tophit)

    def get_all_tracks_from_artist(self, artist_browser):
        print 'getting ALL tracks from this artist.'
        tracks = []
        added_albums = []
        for album in artist_browser.albums:
            if album.artist==artist_browser.artist:
                if album.name in added_albums: continue
                tracks = tracks + list(album.browse().load().tracks)
                added_albums.append(album.name)
        return list(tracks)

    def get_tracks_from_one_album(self, album_search_string, artist_browser):
        print 'trying to get that album.'
        album_words = album_search_string.split()
        album = None
        for this_album in artist_browser.albums:
            this_album_name = this_album.name.lower()
            score = 0.
            possible_score = 0.
            for word in album_words:
                if word.lower() in this_album_name: score += len(word)
                possible_score += len(word)
            frac_score = score/possible_score
            if ((score>2) & (frac_score>0.5)):
                album = this_album
                print '  album: %s --- %s'%(
                    album_search_string.encode('utf-8'), 
                    this_album.name.encode('utf-8'))
                break
        # if we couldn't find that album, let's grab the 
        # "top hit" tracks from this artist.
        if album==None:
            return self.get_tophit_tracks_from_artist(artist_browser)
        album_browser = album.browse().load()
        if len(album_browser.tracks)==0: return []
        return list(album_browser.tracks)

    def load_this_playlist(self, playlist_name):
        playlists = self.session.playlist_container.load()
        for playlist in playlists:
            if playlist.name==playlist_name:
                return playlist
        print 'creating new playlist %s'%(playlist_name)
        return playlists.add_new_playlist(playlist_name)

    def add_tracks_to_playlists(self, playlist_prefix):
        nmax_tracks = 500
        ntracks = len(self.tracks)
        imin = 0
        imax = nmax_tracks
        iplaylist = 0
        while (imax<ntracks):
            these_tracks = self.tracks[imin:imax]
            playlist_name = '%s%i'%(playlist_prefix, iplaylist)
            self.add_tracks_to_one_playlist(these_tracks, playlist_name)
            iplaylist += 1
            imin += nmax_tracks
            imax += nmax_tracks
        imax = ntracks
        these_tracks = self.tracks[imin:imax]
        playlist_name = '%s%i'%(playlist_prefix, iplaylist)
        self.add_tracks_to_one_playlist(these_tracks, playlist_name)        

    def add_tracks_to_one_playlist(self, these_tracks, playlist_name):
        from time import sleep
        playlist = self.load_this_playlist(playlist_name)
        while playlist.has_pending_changes: sleep(0.1)
        print 'adding %i tracks to %s'%(len(these_tracks), playlist_name)
        playlist.add_tracks(these_tracks)
        while playlist.has_pending_changes: sleep(0.1)

    def viz_tracks_to_add(self):
        print ' '
        for track in self.tracks:
            print '%s --- %s'%(track.artists[0].name.encode('utf-8'), 
                               track.name.encode('utf-8'))
        print ' '


if __name__ == "__main__":
    main()
