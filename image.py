import requests
import random

def get_image_url(query):

    r = requests.get("https://api.qwant.com/api/search/images",
        params={
            'count': 50,
            'q': query,
            't': 'images',
            'safesearch': 1,
            'locale': 'en_US',
            'uiv': 4
        },
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        }
    )


    response = r.json().get('data').get('result').get('items')
    urls = [r.get('media') for r in response]
    return random.choice(urls)


def get_image(query, lyrics):
    from PIL import Image, ImageDraw, ImageFont
    import requests
    from io import BytesIO
    url = get_image_url(query)
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    newsize = (900, 600) 
    img = img.resize(newsize)
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype('Impact.ttf', 35)
    d.text((20,400), lyrics, font=fnt, fill=(255,255,255))
    
    img.save('test.png')