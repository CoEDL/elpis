import os

from flask import Flask
from . import corpus


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder='static')

    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    app.register_blueprint(corpus.bp)

    @app.route('/')
    def hello():
        return 'Hello, world'

    return app
