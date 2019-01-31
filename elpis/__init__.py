import os

from flask import Flask, redirect
from . import corpus

# Setup paths
ELPIS_ROOT_DIR = os.getcwd()
GUI_ROOT_DIR = os.path.join(ELPIS_ROOT_DIR, "elpis-gui/build")
GUI_PUBLIC_DIR = GUI_ROOT_DIR
GUI_STATIC_DIR = os.path.join(GUI_ROOT_DIR, "js")
MODELS_DIR = os.path.join(ELPIS_ROOT_DIR, 'models')

def create_app(test_config=None):
    if not os.path.exists(MODELS_DIR):
        print('making the dir!')
        os.mkdir(MODELS_DIR)

    # Setup static resources
    # create and configure the app
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder=GUI_STATIC_DIR,
                static_url_path='/js')

    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    app.register_blueprint(corpus.bp)


    @app.route('/index.html')
    def index_file():
        """Redirects to '/' for React."""
        return redirect('/')

    @app.route('/', defaults={'path':''})
    @app.route("/<path:path>")
    def index(path):
        print('in index with:', path)
        with open(f"{GUI_PUBLIC_DIR}/index.html", "r") as fin:
            content = fin.read()
            return content
    
    @app.route('/favicon.ico')
    def favicon():
        with open(f"{GUI_PUBLIC_DIR}/favicon.ico", "rb") as fin:
            return fin.read()

    return app
