import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from .db_model import User
from .twitter import nlp, tweet_vector


def predict_user(user_1, user_2, tweet_text):
    user1 = User.query.filter(User.username == user_1).one()
    user2 = User.query.filter(User.username == user_2).one()
    breakpoint()
    user1_embed = np.array([tweet.embed for tweet in user1.tweets])
    user2_embed = np.array([tweet.embed for tweet in user2.tweets])
    breakpoint()
    embeds = np.vstack([user1_embed, user2_embed])
    labels = np.concatenate([np.ones(len(user1.tweets)),
                             np.zeros(len(user2.tweets))])
    breakpoint()
    knc = KNeighborsClassifier(weights='distance', metric='cosine').fit(embeds, labels)
    embed_tweet = tweet_vector(tweet_text=tweet_text)
    breakpoint()
    return knc.predict(np.array(embed_tweet).reshape(1, -1))
