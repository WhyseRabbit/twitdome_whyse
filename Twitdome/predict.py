import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression
from .db_model import User
from .twitter import nlp, tweet_vector


def predict_user(user_1, user_2, tweet_text):
    user_set = pickle.dumps((user_1, user_2))
    user1 = User.query.filter(User.username == user_1).one()
    user2 = User.query.filter(User.username == user_2).one()
    user1_embed = np.array([tweet.embed for tweet in user1.tweets])
    user2_embed = np.array([tweet.embed for tweet in user2.tweets])

    embeds = np.vstack([user1_embed, user2_embed])
    labels = np.concatenate([np.ones(len(user_1.tweets)),
                             np.zeros(len(user_2.tweets))])

    log_reg = LogisticRegression(max_iter=1000).fit(embeds, labels)
    embed_tweet = tweet_vector(tweet_text=tweet_text)

    return log_reg.predict(np.array(embed_tweet).reshape(1, -1))
