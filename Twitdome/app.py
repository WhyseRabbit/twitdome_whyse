from flask import Flask


def create_app():
    """Create and configure Flask app."""
    app = Flask(__name__)


    @app.route("/")

    def root():
        return "Hello, Twitter Dome!"
    return app

