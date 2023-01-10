import tweepy
import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["API_KEY"]
api_secret = os.environ["API_SECRET"]
# bearer_token = os.environ["BEARER_TOKEN"]
access_token = os.environ["ACCESS_TOKEN"]
access_secret = os.environ["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuth1UserHandler(
    api_key, api_secret, access_token, access_secret
)

api = tweepy.API(auth)

if __name__ == "__main__":
   pages = requests.get("https://wiki.facepunch.com/gmod/~pagelist?format=json")

   f = open("pages.json")
   cached_pages = f.readlines()

   print(type(pages))
   #if pages != cached_pages:

