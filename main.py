# imports
import requests
import os
from dotenv import load_dotenv
import json
from summarizer import Summarizer

load_dotenv()

# CHUNK_SIZE=1024
# # Text-to-speech
# def makeAudio(summarizedcontent):
#     voice_id= "Amy"
#     url = "https://api.elevenlabs.io/v1/text-to-speech/"+voice_id
#
#     headers = {
#         "Accept": "audio/mpeg",
#         "Content-Type": "application/json",
#         "xi-api-key": "<xi-api-key>"
#     }
#
#     data = {
#         "text": summarizedcontent,
#         "model_id": "eleven_monolingual_v1",
#         "voice_settings": {
#             "stability": 0.5,
#             "similarity_boost": 0.5
#         }
#     }
#
#     response = requests.post(url, json=data, headers=headers)
#     with open('output.mp3', 'wb') as f:
#         for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
#             if chunk:
#                 f.write(chunk)


# Summarizing text
def summarizedNews(text):
    model = Summarizer()
    result = model(text, ratio=0.2)
    full = ''.join(result)
    return full


# calling news API and getting the content of a sample news article (ex: on blockchain)
def getNews():
    # key = SECRET_KEY
    key = os.getenv("NEWS_API_KEY")
    url = "https://newsdata.io/api/1/news?"
    params = {
        "country": "in",
        "timeframe": "24"
    }

    headers = {
        "X-ACCESS-KEY": key,
        "Content-Type": "application/json"
    }
    # Make a get request with the parameters.
    response = requests.get(url, params=params, headers=headers)

    data = response.text
    convert_json = json.loads(data)
    articles = convert_json['results']

    for article in articles:
        content = article['content']
        print(summarizedNews(content))
        break

def main():
    getNews()

if __name__ == '__main__':
    main()

