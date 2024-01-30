from flask import Flask, render_template, request
from googleapiclient.discovery import build

app = Flask(__name__)

# Enter your YouTube Data API key here
YOUTUBE_API_KEY = 'AIzaSyAc40ZaPoboXkvPgKvUspAg6vQXAYhxJKo'

def search_videos(query):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=10
    )
    response = request.execute()
    videos = []
    for item in response['items']:
        videos.append({
            'title': item['snippet']['title'],
            'video_id': item['id']['videoId'],
            'thumbnail': item['snippet']['thumbnails']['medium']['url']
        })
    return videos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    videos = search_videos(query)
    return render_template('index.html', videos=videos)

if __name__ == '__main__':
    app.run(debug=True)
