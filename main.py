import json
import random
import time
import tweepy
import os
import requests
from dotenv import load_dotenv
import schedule
from bs4 import BeautifulSoup
import re

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
pages = None


def tweet_random_page():
    random_page_num = random.randint(0, len(pages))
    page = pages[random_page_num]
    url = "https://wiki.facepunch.com/gmod/" + page["address"]
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.content, 'html.parser')
    tweet_title = "not real"

    tweet = "Today's wiki page is "

    for title in soup.find_all("title"):
        tweet_title = re.match(r"(.*?)\s-", title.get_text()).group(1)
        tweet = tweet + tweet_title + "\n"

    description_section = soup.find("div", class_="description_section")
    if description_section:
        for tag in description_section(["a", "p"]):
            tag.unwrap()
        tweet = tweet + description_section.text

    if len(tweet) + len(url) > 280:
        tweet = tweet[:280 - len(url)] + "..."

    tweet = tweet + "\n" + url
    api.update_status(tweet)
    pages.remove(page)

    print("Tweeted tweet: " + tweet_title)


if __name__ == "__main__":
    req = requests.get("https://wiki.facepunch.com/gmod/~pagelist?format=json")
    pages = req.json()

    with open('pages.json', 'w') as file:
        file.write(json.dumps(pages))

    tweet_random_page()
    schedule.every(12).hours.do(tweet_random_page)

    while True:
        schedule.run_pending()
        time.sleep(1)
