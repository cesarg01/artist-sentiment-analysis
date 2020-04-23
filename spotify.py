import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import song_scraper
from textblob import TextBlob

# Load in Spotify credentials from environment.
# Create a .env file and settings.py file to load the environment variables.
# More information at https://pypi.org/project/python-dotenv/
import os
from dotenv import load_dotenv
load_dotenv()


class Spotify:
    """
    Class that uses Spotify API to get information from the artist. 
    """

    def __init__(self):
        # Initialize Spotify API with the credentials
        self.__init_spotify()

    def __init_spotify(self):
        '''
            Log into the Spotify API with the correct client id and secret id.
        '''
        credentials = SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFIY_CLIENT_SECRET'))
        self.token = credentials.get_access_token()
        self.spotify = spotipy.Spotify(self.token)

    def get_artist(self, artist_name):
        """
        Searches the Spotify API for the given artist name,
        and returns an artist with their albums populated.
        """
        try:
            results = self.spotify.search(
                q="artist:" + artist_name,
                limit=1,
                type="artist"
            )
            results = results["artists"]["items"][0]
            
        except Exception as e:
            # Catch token expired exception.
            # Re-initialize Spotify API in case token expired.

            print('Error in get_artist:', e)
            self.__init_spotify()

        artist = {
            'name': results['name'],
            'albums': [],
            'imageURL': results['images'][0]['url'],
            'URL': results['external_urls']['spotify']
        }
        
        # The variable being passed is the artist ID from the JSON data.
        albums = self.get_artist_albums(results['id'])
        
        for album in albums:
            artist['albums'].append(album)
            #print(album)

        return artist

    def get_artist_albums(self, artist_id):
        '''
            Searches the Spotify API to get all the albums from a given artists and gets rid
            of unnecessary albums.
        '''
        print('artist_id:', artist_id)

        # API call to get all the albums names for the artist
        results = self.spotify.artist_albums(artist_id, album_type='album')
        results = results['items']
        
        albums = []
        seen = set()
        counter = 0
        MAX_LIMIT = 2
        # Get the albums names and filter out unnecessary albums (Delux, remixes, etc.)
        print('Printing out the name of the whole album followed by the album id.\n')
        for item in results:
            name, album_id = item['name'], item['id']
            print('Album name:', name)
            print('Album ID:', album_id)

            if name in seen or '(' in name:
                continue
            if counter < MAX_LIMIT:
                seen.add(name)
                counter += 1
                # NOTE: This only creates one album. To create all the albums we must put this inside the for loop
        # above.
                songs = self.get_songs(album_id)
                album = self.create_album(name, songs)
                # NOTE: This a temporary fix when genius doesn't have lyrics. Should fix song_scraper file.
                if(len(album['songs']) == 0):
                    continue
                else:
                    albums.append(album)
            else:
                break
            
        return albums

    def create_album(self, name, songs):
        '''
            Create an album with the songs and add a sentiment index to the album list which holds the total polarity of
            the album.
        '''
        total = 0

        for song in songs:
            total += song['polarity']

        album = {
            'name': name,
            'songs': songs
        }
        if(len(songs) == 0):
            print('Album has no songs and album name is ' + name)

        else:
            album['sentiment'] = total / len(songs)
            print('Length of album is ', len(songs))
        
            
        #print(songs[0]['energy'])
        return album
    
    def get_songs(self, album_id):
        '''
            Gets the songs for album and get the song features we need like polarity, valence, energy, and danceability.
        '''
        results = self.spotify.album_tracks(album_id)
        results = results['items']
        #num_tracks = len(results['items'])

        # Create a dictionary to keep the values of the track (includes track_id, name of song, and lyrics to song)
        values = {}
        songs = []
        for track in results:
            artist = track['artists'][0]['name']
            track_id = track['id']
            values[track_id] = {}
            #print(track['name'])

            lyrics = song_scraper.get_song_lyrics(artist, track['name'])
            values[track_id] = lyrics
            #print(lyrics)
            
            # Skip songs that do not have lyrics since we cannot do polarity analysis.
            # Check to see if the songs can be turned into a URL if not then exit program with message
            # saying could not create song URL.
            try:
                if not values[track_id].get('lyrics'):
                    continue
            except AttributeError as e:
                print('Error in getting song URL', e)
                print('Try another artist. Sorry for the inconvenience.')
                exit()

            polarity = TextBlob(values[track_id]['lyrics']).sentiment.polarity
            #print(track['name'], polarity)
        

            song = {
                'name': values[track_id]['name'],
                'polarity': polarity
            }
        
            songs.append(song)
            #print(songs)
        features = self.get_track_features(values)
        song_ids = list(features.keys())

        # For each song in the list add the features from Spotify into the song dictionary
        for song, id in zip(songs, song_ids):
            song['valence'] = features[id].get('valence')
            song['energy'] = features[id].get('energy')
            song['danceability'] = features[id].get('danceability')
        
        #print(songs)    
        return songs

    def get_track_features(self, songs):
        '''
            Get track features related to energy (Typically, energetic tracks feel fast, loud, and noisy.) and valance
            (Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence 
            sound more negative (e.g. sad, depressed, angry)). A value of 1.0 or closer to 1.0 for each feature means the track is
            very energetic and more positive respectively.
        '''

        # Get the song ids from the dictionary.
        song_ids = list(songs.keys())
        
        #for id in song_ids:
        #    print(songs[id].get('name'))

        # Get all the track features for the whole album.
        feature_set = self.spotify.audio_features(song_ids)

        # For each song get the valence and energy features.
        for song_id, feature in zip(song_ids, feature_set):
            songs[song_id]['valence'] = feature['valence']
            songs[song_id]['energy'] = feature['energy']
            songs[song_id]['danceability'] = feature['danceability']
    
        #for id in song_ids:
        #    print(songs[id].get('name'), songs[id].get('energy'))
            
            #print(songs[id].get('energy'))

        #print(songs)
        return songs


#sp = Spotify()
#results = sp.get_artist('saint asonia')

#print(results)
