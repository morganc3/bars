#!/usr/bin/env python

import time,sys,random

import swagger_client
from swagger_client.rest import ApiException

# str | Account api key, to be used in every api call
swagger_client.configuration.api_key['apikey'] = "ee07e7d4b0e555bce87a751e09ca862c"

# create an instance of the API class
artist_api_instance = swagger_client.ArtistApi()
album_api_instance = swagger_client.AlbumApi()

format = 'json' # str | output format: json, jsonp, xml. (optional) (default to json)

def search_artists(name):
    try: 
        api_response = artist_api_instance.artist_search_get(q_artist=name, format=format)
        artist_list = api_response.message.body.artist_list
        return artist_list
    except ApiException as e:
        print("Exception when calling DefaultApi->album_get_get: %s\n" % e)

def get_albums(id):
    try:
        api_response = album_api_instance.artist_albums_get_get(artist_id=id, format=format)
        album_list = api_response.message.body.album_list
        return album_list
    except ApiException as e:
        print("Exception when calling DefaultApi->album_get_get: %s\n" % e)

#artist_name = input("Enter an artist name: ") 
#artist_search_results = search_artists(artist_name)
artist_search_results = search_artists("beyonce")

#assume first is correct
artist = artist_search_results[0]
albums = get_albums(artist.artist.artist_id)
rand_album_index = random.randint(0,len(albums)-1)
album_id = albums[rand_album_index].album.album_id
album_name = albums[rand_album_index].album.album_name
print(album_id, album_name)

