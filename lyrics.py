import requests
import urllib.parse
import random
from pyquery import PyQuery
import os

genius_api_key = os.getenv("RAPGENIUS_API_KEY")
genius_api_domain = "https://api.genius.com/"
headers = {"Authorization":"Bearer {}".format(genius_api_key)}

def get_artist_id(artist):
    artist = urllib.parse.quote(artist)
    r = requests.get(genius_api_domain+"search?q={}".format(artist), headers=headers)
    return r.json()['response']['hits'][0]['result']['primary_artist']['id']

def get_random_song(artist_id):
    r = requests.get(genius_api_domain+"artists/{}/songs?per_page=40&sort=popularity".format(artist_id), headers=headers)
    songs = r.json()['response']['songs']
    rand_song_id = random.choice(songs)['url']
    return rand_song_id



def get_lyrics(song_url):
    r = requests.get(song_url)
    html_content = r.content.decode('utf-8')
    pq = PyQuery(html_content)
    tag = pq('div.lyrics')
    lyrics = tag.text()
    lyrics = lyrics.split("\n")
    lines_no_brackets = []
    for line in lyrics:
        if '[' not in line and ']' not in line and line != '':
            lines_no_brackets.append(line)
    lines = lines_no_brackets
    line_count = len(lines)
    rand_line = random.randint(0,line_count-2)
    #return a random line and the line after
    return (lines[rand_line], lines[rand_line+1])

    
