import spotipy
# To access authorised Spotify data
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException

import requests
from requests.exceptions import ConnectionError


class MySpotify:
    client_id = 'a9f6f8710a7f41eeb78e65e8f73b0a9a'
    client_secret = '590f8da68c2343eaa2dd2db86dc751e0'

    def __init__(self, **kwargs):
        self.client_credentials_manager = SpotifyClientCredentials(
            client_id=self.client_id, client_secret=self.client_secret)

        # spotify object to access API
        self.sp = spotipy.Spotify(
            client_credentials_manager=self.client_credentials_manager)

    def get_new_releases(self):
        return self.sp.new_releases()

    def search_query(self, query):
        try:
            return self.sp.search(query)

        except SpotifyException:
            return None

        except ConnectionError:
            return "Error"


class Artist(MySpotify):

    def __init__(self, artist_name, **kwargs):
        self.artist_name = artist_name
        super(Artist, self).__init__(**kwargs)

        if artist_name != '':
            # get artist uri for id_ing the artist on the API
            self.artist_uri = self.get_artist_uri(self.artist_name)

            self.artist_image = self.get_artist_image(
                self.artist_name)  # get artist image url

    def get_artist_image(self, artist):
        results = self.sp.search(q='artist:' + artist, type='artist')
        items = results['artists']['items']

        if len(items) > 0:
            artist = items[0]
            artist_image = artist['images'][0]['url']

        else:
            artist_image = ''

        return artist_image

    def get_artist_uri(self, artist):

        result = self.sp.search(artist)  # search query

        artist_uri = result['tracks']['items'][0]['artists'][0]['uri']

        return artist_uri

    def get_top_tracks(self):
        results = self.sp.artist_top_tracks(self.artist_uri)

        self.top_tracks = results['tracks']

        return self.top_tracks

    def get_singles(self):
        results = self.sp.artist_albums(
            self.artist_uri, album_type='single', limit=50)

        tracks = results['items']

        for track in tracks:
            ind = tracks.index(track)

            track_real = self.sp.album_tracks(track['uri'])['items'][0]

            track['popularity'] = self.get_track_popularity(track_real['uri'])

            tracks[ind] = track

        self.singles = tracks

        return tracks

    def get_collabs(self):
        results = self.sp.artist_albums(
            self.artist_uri, album_type='appears_on')

        return results['items']

    def get_albums(self):

        all_albums = {}

        results = self.sp.artist_albums(self.artist_uri, album_type='album')

        self.albums = results['items']

        while results['next']:
            results = self.sp.next(results)
            albums.extend(results['items'])

        return self.albums

class Album(MySpotify):
    def __init__(self, album_uri, **kwargs):
        self.album_uri = album_uri
        super(Album, self).__init__(**kwargs)
        self.get_album()
        self.get_album_popularity()

    def get_album(self):
        self.album = self.sp.album(self.album_uri)      

        result_tracks = self.sp.album_tracks(self.album_uri)

        self.tracks = result_tracks['items']

    def get_track_popularity(self, uri):
        track_res = self.sp.track(uri)
        print(track_res['popularity'])

        return track_res['popularity']

    def get_album_popularity(self):
        total_op = 0

        for track in self.tracks:
            ind = self.tracks.index(track)

            popularity = self.get_track_popularity(track['uri'])

            track['popularity'] = popularity

            total_op += int(popularity)

            self.tracks[ind] = track

        self.popularity_album = total_op/len(self.tracks)

        self.album['popularity'] = self.popularity_album

    def get_track_image(self, track):
        try:
            return track['album']['images'][0]['url']
        except KeyError:
            return track['images'][0]['url']


def download(self, link, file_name, c_size=1024):

    req = requests.get(link, stream=True)
    file_type = req.headers['Content-type']
    print(file_type)

    # get content size in bytes
    file_length = req.headers['Content-length']
    print(file_length)

    with open(file_name, 'wb') as file:  # open file
        downloaded_chunk = 0

        # iter content in chunks specified and right each chunk in file
        for chunk in req.iter_content(chunk_size=c_size):
            if chunk:
                file.write(chunk)
                downloaded_chunk += c_size
                yield (downloaded_chunk / int(file_length)) * 100

'''
 elif action == 'trackpop':
        trackInfo = {}
        trial = 0

        while trial < max_tries
            try:
                my_spotify_obj = MySpotify()                
                track = my_spotify_obj.search_query(query)['tracks']['items'][0]

                trackInfo['popularity']  = track['popularity']
                trackInfo['album']       = track['album']['name'] if 'album' in track else ''
                trackInfo['trackNumber'] = track['track_number'] if 'track_number' in track else ''
                trackInfo['uri']         = track['uri']
                trackInfo['previewUrl']  = track['preview_url']
                trackInfo['url']         = track['href']
                trackInfo['explicit']    = track['explicit']
                trackInfo['isLocal']     = track['is_local']

                return trackInfo

'''