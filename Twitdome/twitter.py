from os import getenv
import tweepy
import spacy
from dotenv import load_dotenv
from .db_model import DB, User, Tweet


load_dotenv()

TWITTER_API_KEY = getenv("TWITTER_API_KEY", default="NUH_UH!")
TWITTER_SECRET_API = getenv("TWITTER_SECRET_API", default="NUH_UH!")
TWITTER_ACCESS_TOKEN = getenv("TWITTER_ACCESS_TOKEN", default="NUH_UH!")
TWITTER_ACCESS_SECRET = getenv("TWITTER_ACCESS_SECRET", default="NUH_UH!")

TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_SECRET_API)
TWITTER_AUTH.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
TWITTER = tweepy.API(TWITTER_AUTH)

spacy_model_name = "en_core_web_sm"
if not spacy.util.is_package(spacy_model_name):
    spacy.cli.download(spacy_model_name)

nlp = spacy.load(spacy_model_name, disable=["tagger", "parser"])
def tweet_vector(tweet_text):
    return nlp(tweet_text).vector

def add_user_tweepy(username):
    """Add a user and their tweets to database"""
    try:
        twitter_user = TWITTER.get_user(username)

        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id,
                        username=username,
                        followers=twitter_user.followers_count))

        DB.session.add(db_user)

        tweets = twitter_user.timeline(count=200,
                                       exclude_replies=True,
                                       include_rts=False,
                                       tweet_mode="extended",
                                       full_text=True,
                                       since_id=db_user.newest_tweet_id)

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:

            embed = tweet_vector(tweet.full_text)

            db_tweet = Tweet(id=tweet.id,
                             text=tweet.full_text[:300],
                             embed=embed)
            db_user.tweet.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print(f"Error processing {username}: {e}")
        raise e

    else:
        DB.session.commit()


def add_user_history(username):
    """Add max tweet history (API limit of 3200) to database"""
    try:
        twitter_user = TWITTER.get_user(username)

        db_user = (User.query.get(twitter_user.id) or
                   User(id=twitter_user.id,
                        username=username,
                        followers=twitter_user.followers_count))
        DB.session.add(db_user)

        tweets = twitter_user.timeline(count=200,
                                       exclude_replies=True,
                                       include_rts=False,
                                       tweet_mode="extended",
                                       full_text=True)
        oldest_max_id = tweets[-1].id - 1
        tweet_history = []
        tweet_history += tweets

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        while True:
            tweets = twitter_user.timeline(count=200,
                                           exclude_replies=True,
                                           include_rts=False,
                                           tweet_mode="extended",
                                           full_text=True,
                                           max_id=oldest_max_id)
            if len(tweets) == 0:
                break

            oldest_max_id = tweets[-1].id - 1
            tweet_history += tweets

        print(f"Total Tweets collected for {username}: {len(tweet_history)}")

        for tweet in tweet_history:
            embed = tweet_vector(tweet.full_text)

            db_tweet = Tweet(id=tweet.id,
                             text=tweet.full_text[:300],
                             embed=embed)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)

    except Exception as e:
        print(f"Error processing {username}: {e}")
        raise e

    else:
        DB.session.commit()
        print("Successfully saved tweets to DB!")


def update_users():
    for user in User.query.all():
        add_user_tweepy(user.username)
