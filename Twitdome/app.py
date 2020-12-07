from flask import Flask, render_template, request
from .db_model import DB, User, Tweet
from .twitter import add_user_tweepy
from .predict import predict_user


def create_app():
    """Create and configure Flask app."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Twitdome.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    @app.route("/")
    def root():
        return render_template("base.html", title="TwitDome Home", users=User.query.all())
    
    @app.route("/user", methods=["POST"])
    @app.route("/user/<name>", methods=["GET"])
    def add_or_update_user(name=None, message=""):
        """Adds User to User-class DataBase."""

        name = name or request.values["user_name"]

        try:

            if request.method == "POST":
                add_user_tweepy(name)
                message = "User {} has been added to the Twitter Dome!".format(name)

            tweets = User.query.filter(User.username == name).one().tweet

        except Exception as e:
            print("{} is not worthy!: {}".format(name, e))
            tweets = []

        return render_template("user.html", title=name, tweets=tweets, message=message)

    
    @app.route("/compare", methods=["POST"])
    def compare(message=""):
        """This page predicts which user is more likely to say what."""
        user1 = request.values["user1"]
        user2 = request.values["user2"]
        tweet_text = request.values["tweet_text"]

        if user1 == user2:
            message = f"{user1}, now is not the time for existential crisis!"
        else:
            prediction = predict_user(user1, user2, tweet_text)

            message = f"""{user1 if prediction else user2} just dropped the finishing blow
            on {user2 if prediction else user1} with weapon: {tweet_text}"""

        return render_template("predict.html", title="Prediction", message=message)

    
    @app.route("/reset")
    def reset():
        """Resets the DataBase for a clean start."""
        DB.drop_all()
        DB.create_all()

    return app
