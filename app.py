from random import randrange

from apiclient.discovery import build

import requests
from flask import Flask, render_template, request

DISCOGS_TOKEN = 'JLyawlHOYLPCOPyRQqVoASPqzwJAgRjldmGUNJwA'
GOOGLE_API_KEY = 'AIzaSyBoaF8Iw2iP617qopJSC1N1QtDJiq4_Wk8'

app = Flask(__name__)


@app.route('/album-cover')
def album_cover():
    artist = request.args.get('artist')

    response = requests.get(
        'https://api.discogs.com/database/search?artist=' + artist + '&type=master&format=LP',
        headers={'Authorization': ('Discogs token=%s' % DISCOGS_TOKEN)}
    )
    print('Status code:', response.status_code)
    print('Headers:', response.headers)

 

    response_json = response.json()
    print(response_json)  # print the entire JSON response

    if 'results' not in response_json:
        return "No 'results' in JSON response"

    number_of_hits = len(response.json()['results'])
    if number_of_hits == 0:
        return render_template('artist-not-found.html', artist=artist, showmode=True)

    random_entry = response.json()['results'][randrange(number_of_hits)]

    return render_template('index.html', artist=artist, uri=random_entry['cover_image'], title=random_entry['title'], showmode=True)


@app.route('/youtube')
def youtube():
    return render_template('index.html',
                           artist=(request.args.get('artist')),
                           uri=(request.args.get('imageUri')),
                           title=(request.args.get('title')),
                           videolink=youtubeid(request.args.get('title')),
                           showmode=False)


def youtubeid(title):
    youtube = build("youtube", "v3", developerKey=GOOGLE_API_KEY)

    try:
        search_response = youtube.search().list(q=title, part="id,snippet", maxResults=1).execute()
        for search_result in search_response.get("items", []):
            if search_result["id"]["kind"] == "youtube#video":
                return search_result["id"]["videoId"]
    except Exception as e:
        print(e)
