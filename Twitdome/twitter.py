import os
from dotenv import load_dotenv
import tweepy


load_dotenv()

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", default="NUH_UH!")
TWITTER_SECRET_API = os.getenv("TWITTER_SECRET_API", default="NUH_UH!")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", default="NUH_UH!")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET", default="NUH_UH!")

TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET_API)
TWITTER_AUTH.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)
