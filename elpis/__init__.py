import os

from flask import redirect
from . import api
from .app import Flask

from .paths import GUI_STATIC_DIR, GUI_PUBLIC_DIR

from .kaldi.interface import KaldiInterface
from pathlib import Path

def create_app(test_config=None):

    # Setup static resources
    # create and configure the app
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder=GUI_STATIC_DIR,
                static_url_path='/js')

    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    interface_path = Path('/root/.local/share/elpis/test')
    if not interface_path.exists():
        app.config['INTERFACE'] = KaldiInterface(interface_path)
    else:
        app.config['INTERFACE'] = KaldiInterface.load(interface_path)
    app.config['CURRENT_DATABUNDLE'] = None
    app.config['CURRENT_MODEL'] = None
    
    app.register_blueprint(api.bp)
    print(app.url_map)


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
