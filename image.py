import requests
import random
from googleapiclient.discovery import build

from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

import os
api_key = os.getenv("GOOGLE_API_KEY")
cse = os.getenv("GOOGLE_CSE")

fnt = ImageFont.truetype('Impact.ttf', 42)
img_width = 600
img_height = 450

# take a line and return a list of shorter lines that can be written to the image
def format_lines(line):
    # character count before newline
    increment = 25
    pos = 0
    line_len = len(line)
    toRet = []
    lines_count = 0

    while pos < line_len:
        end_line_pos = pos+increment
        while end_line_pos < len(line) and line[end_line_pos] != ' ':
            # increment by 1 until we get to the end of a word
            # so that the newline doesn't split in the middle of a word
            end_line_pos = end_line_pos + 1
        
        lines_count = lines_count + 1
        toRet.append('\n'*lines_count + line[pos:end_line_pos])
        

        if end_line_pos < line_len:
            if line[end_line_pos] == ' ':
                # skip the space so next line doesn't start with a space
                end_line_pos = end_line_pos + 1
        pos = end_line_pos

    return toRet


def get_image_url(artist):

    service = build("customsearch", "v1",
                  developerKey=api_key)

    # get search results 1-10
    res1 = service.cse().list(
        q=artist,
        cx=cse,
        searchType='image',
        ).execute()

    # get search results 10-20
    res2 = service.cse().list(
        q=artist,
        cx=cse,
        searchType='image',
        start=11
        ).execute()

    items1 = res1.get('items')
    items2 = res2.get('items')
    items = items1 + items2
    random_url = random.choice(items)['link']
    return random_url


def get_image(url, lyrics):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    newsize = (img_width, img_height) 
    img = img.resize(newsize)
    d = ImageDraw.Draw(img)
    write_line(d,lyrics[0], top=True)
    write_line(d,lyrics[1])
    return img

def drawTextWithOutline(draw, text, x, y):
    draw.text((x-2, y-2), text,(0,0,0),font=fnt)
    draw.text((x+2, y-2), text,(0,0,0),font=fnt)
    draw.text((x+2, y+2), text,(0,0,0),font=fnt)
    draw.text((x-2, y+2), text,(0,0,0),font=fnt)
    draw.text((x, y), text, (255,255,255), font=fnt)

def write_line(draw, line, top=False):
    formatted_lines = format_lines(line)
    for formatted_line in formatted_lines:
        w, _ = draw.textsize(formatted_line, fnt)
        height_position = 0
        if top:
            height_position = -50
        else:
            height_position = 300

        drawTextWithOutline(draw, formatted_line, img_width/2 - w/2, height_position)


