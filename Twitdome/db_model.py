from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()


class User(DB.Model):
    """This is a backend database that stores Twitter users with their newest tweet id."""
    id = DB.Column(DB.BigInteger, primary_key=True)
    username = DB.Column(DB.String(80), unique=True, nullable=False)
    followers = DB.Column(DB.String(100), unique=True, nullable=False)
    tweets = DB.Column(DB.Unicode(280), unique=True, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger, nullable=False)

    def __repr__(self):
        return "<User %r>" % self.name


class Tweet(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    text = DB.Column(DB.Unicode(280), unique=True, nullable=False)
    embed = DB.Column(DB.PickleType, nullable=False)
    user_id = DB.Column(DB.Integer, DB.ForeignKey("user.id"), nullable=False)
    user = DB.relationship("User", backref=DB.backref("text", lazy=True))

    def __repr__(self):
        return "<Tweet %r>" % self.text

# flask shell
# >>> from Twitdome.db_model import DB, User, Tweet
# >>> DB.create_all()
# >>> user1 = User(username="BarackObama")
# >>> user2 = User(username="1JimmyTheRabbit")
# >>> tweet1 = Tweet(text="President, White House, and The United States of America.")
# >>> tweet2 = Tweet(text="The Secret is coming for you...")
# >>> user1.tweets.append(tweet1)
# >>> user2.tweets.append(tweet2)
# >>> DB.session.add(user1)
# >>> DB.session.add(user2)
# >>> DB.session.commit()