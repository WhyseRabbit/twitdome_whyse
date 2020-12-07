from flask import Flask, render_template
from .db_model import DB, User


def create_app():
    """Create and configure Flask app."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Twitdome.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    DB.init_app(app)

    @app.route("/")
    def root():
        return "Hello, Twitter Dome!"
    
    @app.route("/<username>")
    def add_user(username):
        """Adds User to User-class DataBase."""
        user = User(username=username)
        DB.session.add(user)
        DB.session.commit()
        return f"{username} has entered the Dome!"

    return app
