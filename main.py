from lyrics import get_artist_id, get_random_song, get_lyrics
from image import get_image, get_image_url
from flask_api import status
from flask import send_file, Flask
import tempfile
import threading
import os
import discord 

app = Flask(__name__)

DISCORD_TOKEN=os.getenv("DISCORD_TOKEN")

@app.route('/<artist>')
def generate_image(artist):
    try:
        artist_id = get_artist_id(artist)
        song_url = get_random_song(artist_id)
        lyrics = get_lyrics(song_url)

        image_url = get_image_url(artist)
        image = get_image(image_url, lyrics)
        tf = tempfile.NamedTemporaryFile()
        file_name = tf.name + '.png'
        image.save(file_name)
        response = send_file(file_name, mimetype='image/png')
        response.cache_control.max_age = 0
        return response

    except:
        return "error", status.HTTP_500_INTERNAL_SERVER_ERROR

def create_server():
      app.run(host='0.0.0.0', port=80)

# start flask server
threading.Thread(target=create_server).start()


client = discord.Client()

@client.event
async def on_message(message):
    if '!bars' in message.content.lower():
        try:
            artist = message.content[6:]
            artist_id = get_artist_id(artist)
            song_url = get_random_song(artist_id)
            lyrics = get_lyrics(song_url)

            image_url = get_image_url(artist)
            image = get_image(image_url, lyrics)
            tf = tempfile.NamedTemporaryFile()
            file_name = tf.name + '.png'
            image.save(file_name)
            await message.channel.send('🔥🔥🔥🔥')
            await message.channel.send(file=discord.File(file_name))

        except:
            print('error')

client.run(DISCORD_TOKEN)
