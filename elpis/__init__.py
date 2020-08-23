import os
from flask import redirect
from . import endpoints
from .app import Flask
from elpis.engines import Interface
from pathlib import Path


def create_app(test_config=None):
    # Called by the flask run command in the cli.
    GUI_PUBLIC_DIR = "/elpis-gui/build"

    # Setup static resources
    # create and configure the app
    # auto detect for yarn watch or yarn build
    static_dir_watch = '/js'
    static_dir_build = '/static'
    if 'js' in os.listdir(GUI_PUBLIC_DIR):
        # using yarn watch
        static_dir = static_dir_watch
    else:
        static_dir = static_dir_build

    # if os.environ.get('FLASK_ENV') == 'production':
    #     static_dir = static_dir_build
    # else:
    #     static_dir = static_dir_watch
    # Create a custom Flask instance defined in the app.py file. Same as a
    # normal Flask class but with a specialised blueprint function.
    app = Flask(__name__,
                instance_relative_config=True,
                static_folder=GUI_PUBLIC_DIR + static_dir,
                static_url_path=static_dir)

    # When making this multi-user, the secret key would require to be a secure hash.
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    elpis_path = Path(os.getcwd())
    app.config['ELPIS_PATH'] = elpis_path

    # For a single user, storing the interface object is okay to do in
    # the app.config, however, this would need to change for multi-user.
    # Each user would require a unique Interface. One Interface
    # stores all the artifacts that user has generated.
    interface_path = Path(os.path.join(elpis_path, '/state'))
    if not interface_path.exists():
        app.config['INTERFACE'] = Interface(interface_path)
    else:
        app.config['INTERFACE'] = Interface(interface_path, use_existing=True)
    # app.config['CURRENT_DATASET'] = None # not okay for multi-user
    # app.config['CURRENT_PRON_DICT'] = None # not okay for multi-user & need to remove later because it is Kaldi-specific.
    # app.config['CURRENT_MODEL'] = None # not okay for multi-user
    # app.config['CURRENT_TRANSCRIPTION'] = None  # not okay for multi-user

    # add the endpoints routes
    app.register_blueprint(endpoints.bp)
    # print(app.url_map)

    # the rest of the routes below are for the single file react app.
    @app.route('/index.html')
    def index_file():
        """Redirects to '/' for React."""
        return redirect('/')

    @app.route('/', defaults={'path': ''})
    @app.route("/<path:path>")
    def index(path):
        with open(f"{GUI_PUBLIC_DIR}/index.html", "r") as fin:
            content = fin.read()
            return content

    @app.route('/favicon.ico')
    def favicon():
        with open(f"{GUI_PUBLIC_DIR}/favicon.ico", "rb") as fin:
            return fin.read()

    return app
