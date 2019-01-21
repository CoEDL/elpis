import os

from flask import Flask
from . import corpus
# from . import static

GUI_ROOT_DIR = os.path.join(os.getcwd(), "elpis-gui/build")
GUI_PUBLIC_DIR = GUI_ROOT_DIR
GUI_STATIC_DIR = os.path.join(GUI_ROOT_DIR, "static")

def create_app(test_config=None):
    print(os.getcwd())
    # Setup static resources
    # create and configure the app
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder=GUI_STATIC_DIR,
                static_url_path='/static')

    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    app.register_blueprint(corpus.bp)
    # app.register_blueprint(corpus.bp)

    @app.route('/')
    @app.route('/index.html')
    def index():
        with open(f"{GUI_PUBLIC_DIR}/index.html", "r") as fin:
            content = fin.read()
            print(content)
            return content
    
    @app.route('/favicon.ico')
    def favicon():
        with open(f"{GUI_PUBLIC_DIR}/favicon.ico", "rb") as fin:
            return fin.read()

    return app
