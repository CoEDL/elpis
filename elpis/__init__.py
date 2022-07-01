import os
import logging
from loguru import logger

from flask import redirect
from . import endpoints
from .app import Flask
from elpis.engines import Interface
from pathlib import Path
from requests import get
from dotenv import load_dotenv
from tensorboard import program
import psutil
from werkzeug.serving import is_running_from_reloader


def create_app(test_config=None):
    # Called by the flask run command in the cli.
    GUI_BUILD_DIR = "/elpis/elpis/gui/build"
    GUI_PUBLIC_DIR = "/elpis/elpis/gui/public"

    # Variable to control the use of a proxy to support webpackdevserver
    WEBPACK_DEV_SERVER_PROXY = os.environ.get("WEBPACK_DEV_SERVER_PROXY", None)

    log = logging.getLogger("werkzeug")
    log.setLevel(logging.DEBUG)
    # Prevent the HTTP request logs polluting more important train logs
    log.disabled = True

    if WEBPACK_DEV_SERVER_PROXY:
        app = Flask(__name__, instance_relative_config=True, static_folder=GUI_PUBLIC_DIR)
    else:
        # Setup static resources
        # create and configure the app
        # auto detect for yarn watch or yarn build
        static_dir_watch = "/js"
        static_dir_build = "/static"
        if "js" in os.listdir(GUI_BUILD_DIR):
            # using yarn watch
            static_dir = static_dir_watch
        else:
            static_dir = static_dir_build

        # if os.environ.get('FLASK_ENV') == 'production':
        #     static_dir = static_dir_build
        # else:
        #     static_dir = static_dir_watch
        logger.info(f"using static_dir: {static_dir}")
        # Create a custom Flask instance defined in the app.py file. Same as a
        # normal Flask class but with a specialised blueprint function.
        app = Flask(
            __name__,
            instance_relative_config=True,
            static_folder=GUI_BUILD_DIR + static_dir,
            static_url_path=static_dir,
        )

    # When making this multi-user, the secret key would require to be a secure hash.
    app.config.from_mapping(SECRET_KEY="dev")

    elpis_path = Path(os.getcwd())
    app.config["ELPIS_PATH"] = elpis_path

    # For a single user, storing the interface object is okay to do in
    # the app.config, however, this would need to change for multi-user.
    # Each user would require a unique Interface. One Interface
    # stores all the artifacts that user has generated.
    interface_path = Path(os.path.join(elpis_path, "/state/of_origin"))
    if not interface_path.exists():
        app.config["INTERFACE"] = Interface(interface_path)
    else:
        app.config["INTERFACE"] = Interface(interface_path, use_existing=True)

    # Developer-friendly mode has convenient interface widgets for setting engine etc
    load_dotenv()
    app.config["DEV_MODE"] = os.environ.get("DEV_MODE")

    # add the endpoints routes
    app.register_blueprint(endpoints.bp)
    # print(app.url_map)

    if is_running_from_reloader():
        # Start Tensorboard if not already running (because Flask init happens twice)
        tensorboard_running = False
        for proc in psutil.process_iter():
            for conns in proc.connections(kind="inet"):
                if conns.laddr.port == 6006:
                    tensorboard_running = True
                    print("Tensorboard is running on", proc.pid)
        if not tensorboard_running:
            print("Tensorboard is not running, start it")
            tensorboard = program.TensorBoard()
            tensorboard.configure(
                argv=[
                    "tensorboard",
                    "--logdir=/state/of_origin/models",
                    "--port=6006",
                    "--host=0.0.0.0",
                ]
            )
            url = tensorboard.launch()
            print(f"Tensorflow listening on {url}")

    # the rest of the routes below are for the single file react app.
    @app.route("/index.html")
    def index_file():
        """Redirects to '/' for React."""
        return redirect("/")

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def index(path):
        logger.info(f"in index with: {path}")
        if WEBPACK_DEV_SERVER_PROXY:
            # If we are running the webpack dev server,
            # We proxy webpack requests through to the dev server
            return proxy("http://localhost:3000/", path)
        else:
            with open(f"{GUI_BUILD_DIR}/index.html", "r") as fin:
                content = fin.read()
                return content

    @app.route("/favicon.ico")
    def favicon():
        with open(f"{GUI_PUBLIC_DIR}/favicon.ico", "rb") as fin:
            return fin.read()

    return app


# Proxy Wrapper
def proxy(host, path):
    response = get(f"{host}{path}")
    excluded_headers = [
        "content-encoding",
        "content-length",
        "transfer-encoding",
        "connection",
    ]
    headers = {
        name: value
        for name, value in response.raw.headers.items()
        if name.lower() not in excluded_headers
    }
    return response.content, response.status_code, headers
