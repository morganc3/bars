#!/usr/bin/env python

import time,sys,random
import image
import swagger_client
from swagger_client.rest import ApiException

# str | Account api key, to be used in every api call
swagger_client.configuration.api_key['apikey'] = "ee07e7d4b0e555bce87a751e09ca862c"

# create an instance of the API class
artist_api_instance = swagger_client.ArtistApi()
album_api_instance = swagger_client.AlbumApi()
track_api_instance = swagger_client.TrackApi()
lyrics_api = swagger_client.LyricsApi()


format = 'json' # str | output format: json, jsonp, xml. (optional) (default to json)

def search_artists(name):
    try: 
        api_response = artist_api_instance.artist_search_get(q_artist=name, format=format)
        artist_list = api_response.message.body.artist_list
        return artist_list
    except ApiException as e:
        print("Exception when calling DefaultApi->album_get_get: %s\n" % e)

def get_albums(artist_id):
    try:
        api_response = album_api_instance.artist_albums_get_get(artist_id=artist_id, page_size=100, format=format)
        album_list = api_response.message.body.album_list
        return album_list
    except ApiException as e:
        print("Exception when calling DefaultApi->album_get_get: %s\n" % e)

def get_album_tracks(album_id):
    import requests
    r = requests.get('https://api.musixmatch.com/ws/1.1/album.tracks.get?album_id={}&page=1&page_size=100&f_has_lyrics=true&apikey=ee07e7d4b0e555bce87a751e09ca862c'.format(str(album_id)))
    return r.json()['message']['body']['track_list']
    # try:
    #     api_response = track_api_instance.album_tracks_get_get(album_id=str(album_id), page_size=1,page=1)
    #     print(api_response)
    #     track_list = api_response.message.body.track_list
    #     return track_list
    # except ApiException as e:
    #     print("Exception when calling DefaultApi->album_get_get: %s\n" % e)

def get_lyrics(track_id):
    import requests
    r = requests.get('https://api.musixmatch.com/ws/1.1/track.lyrics.get?&apikey=ee07e7d4b0e555bce87a751e09ca862c&track_id={}'.format(str(track_id)))
    return r.json()['message']['body']['lyrics']['lyrics_body']


artist_name = input("Enter an artist name: ") 
artist_search_results = search_artists(artist_name)
#artist_search_results = search_artists(artist_name)
print("Generating image for: ")
#assume first is correct
artist = artist_search_results[0]

twitter = artist.artist.artist_twitter_url
albums = get_albums(artist.artist.artist_id)
if len(albums) > 1:
    rand_album_index = random.randint(0,len(albums)-1)
else:
    rand_album_index = 0
album_id = albums[rand_album_index].album.album_id
album_name = albums[rand_album_index].album.album_name
print('\t'+album_name)

track_list = get_album_tracks(album_id)
if len(track_list) > 1:
    rand_track_index = random.randint(0, len(track_list)-1)
else:
    rand_track_index = 0
track_id = track_list[rand_track_index]['track']['track_id']
track_name = track_list[rand_track_index]['track']['track_name']
print('\t'+track_name)


lyrics = get_lyrics(track_id)
lines = lyrics.split('\n')[:-3]

lines_count = len(lines)
rand_lines_index = random.randint(1,lines_count-2)

lyrics = ''
lyrics += lines[rand_lines_index-1] + '\n'
lyrics += lines[rand_lines_index]  + '\n'
lyrics += lines[rand_lines_index+1]  + '\n'
lyrics += lines[rand_lines_index+2]  + '\n'

image.get_image(artist_name, lyrics)