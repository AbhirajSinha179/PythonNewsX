# NewsX
#
# Firstly getting the news title, content and metadata from a news API,
# then summarizing it to have a certain amount of words (in order to reduce video runtime)
# Using elevenlabs text-to-speech to get an audio version of the news
#
# Implementing Wav2Lip lip-sync by the response audio received from tts
#
# Final video generated will be uploaded to YT using Data API v3 and GCP auth
#
# Since the entire pipeline requires each task to be resolved before being completed
# and due to various API monetary restrictions, we'll upload videos


# imports
import requests
import os
from dotenv import load_dotenv
import json
from summarizer import Summarizer

load_dotenv()

CHUNK_SIZE=1024
# Text-to-speech, audio saved to output.mp3 at root level of the directory,, to be used for text-to-avatar
def makeAudio(summarizedcontent):

    key = os.getenv("ELEVENLABS_API_KEY")
    # voice ID of american ground news reporter
    voice_id = "5Q0t7uMcjvnagumLfvZi"
    url = "https://api.elevenlabs.io/v1/text-to-speech/"+voice_id

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": key
    }
    # for hindi news switch to multilingual model, check if v1 or v2 works better
    data = {
        "text": summarizedcontent,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, json=data, headers=headers)
    with open('output.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)


# Summarizing text
def summarizedNews(text):
    # bert model summarizer
    model = Summarizer()
    # need to make sure ratio is not getting neglected,
    # if so, use num_sentences=10 so that lapses in words do not occur
    result = model(text, ratio=0.2)
    full = ''.join(result)
    return full


# calling news API and getting the content of a sample news article (ex: on blockchain)
def getNews():
    key = os.getenv("NEWS_API_KEY")
    url = "https://newsdata.io/api/1/news?"

    # latest news from past 24 hours from US for testing (to get english articles)
    # look to get indian news / hindi articles as well
    params = {
        "country": "us",
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

    # returning the articles dict
    return articles

def main():
    # get the dict of articles
    news_articles = getNews()
    # summarizing topmost article
    summ = summarizedNews(news_articles[0]['content'])
    # text to speech audio generated
    makeAudio(summ)

if __name__ == '__main__':
    main()

