from lyrics import get_artist_id, get_random_song, get_lyrics
from image import get_image, get_image_url
from flask_api import status
from flask import send_file
import tempfile


def generate_image(request):
    try:
        artist = request.args.get('q')
        artist_id = get_artist_id(artist)
        song_url = get_random_song(artist_id)
        lyrics = get_lyrics(song_url)

        image_url = get_image_url(artist)
        image = get_image(image_url, lyrics)
        tf = tempfile.NamedTemporaryFile()
        file_name = tf.name + '.png'
        image.save(file_name)
        response = send_file(file_name, mimetype='image/png')
        headers = {
            "Cache-Control" : "no-cache, no-store, must-revalidate, public, max-age=0"
        }
        return (response, 200, headers)
    except:
        return "error", status.HTTP_500_INTERNAL_SERVER_ERROR

