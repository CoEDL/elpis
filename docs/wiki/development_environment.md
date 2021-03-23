# Developing in VSCode

**Note: this guide is not up to date with the monorepo structure** 

Developing Elpis can be difficult at times as the software is run in a Docker container. This Docker container simplifies the installation of Elpis and its dependencies, but it also adds a barrier to quality development experience as the Python runtime and the code base are all on the container and not easily accessible on the local OS.

In the past, developers mounted volumes, exposed ports and ran commands in terminals connected to the Docker image. With Elpis changing frequently, all these commands change as well and it is easy to lose track.

This tutorial aims to bring about the best possible development experience by setting up the VSCode editor to enable:
* Python linting
* Debugging with breakpoints and variable watching
* IntelliSense
* Unit testing
* Simple terminal access to the Docker container

This works by using VSCode extensions that install another layer on-top of the Elpis image that runs a VSCode server that allows the editor access to the Python runtime and seamless access to the container.

![s](assets/dev-in-vscode/architecture-containers.png)
[1]

## 1. Install Docker and VSCode

Download VSCode ([Link](https://code.visualstudio.com/)).

Make a Docker account and download Docker ([Link](https://www.docker.com/products/docker-desktop)).

## 2. Install Extensions

Open VSCode, then open the Extentions pannel on the left side bar. In the search box at the top of the pannel, search for and install:
 * Docker
 * Python
 * Remote - Containers
 * Remote - SSH
 * Remote - SSH: Editing Configuration Files
 * Remote - SSH: Explorer
 * Remote - WSL (if you're working on windows)

![VSCode Extentions](assets/dev-in-vscode/vsc-extentions.png)

## 3. Clone Repository

Setup your project directory.

1. `mkdir elpis-project && cd elpis-project`

Clone Elpis.

2. `git clone https://github.com/CoEDL/elpis.git`

If you are planning on developing the Elpis GUI clone it as well.

3. `git clone https://github.com/CoEDL/elpis-gui.git`
4. `cd elpis-gui`
5. `npm install`
6. `npm run build`

Your final directory structure should look something like this with the two repositories side by side.

```
elpis-project
├── elpis
└── elpis-gui
```

NOTE: The following setup instructions assume that you follow these instructions for cloning the repository.

## 4. Add `devcontainer.json`

In the `elpis-project/elpis` directory, create a folder called `.devcontainer`. In `.devcontainer` create a file called `devcontainer.json`, which specifies how the VSCode editor will connect to the Docker container. The file contents are:

```json
{
    "name": "Elpis Dev Container (in progress)",
    "image": "coedl/elpis:latest",
    "workspaceFolder": "/elpis",
    "mounts": ["type=bind,source=${localWorkspaceFolder},target=/elpis"],
    
	"settings": { 
		"terminal.integrated.shell.linux": "/bin/zsh",
		"python.pythonPath": "/venv/bin/python3",
		"python.linting.pylintEnabled": true,
		"python.linting.pylintPath": "/venv/bin/pylint",
		"python.linting.enabled": true
	},

	"extensions": [
		"ms-python.python"
	]
}
```

## 5. Re-open VSCode in the Container

We are now ready to open the VSCode in the container. The first time this happens, Docker will need to build the container from the beginning. For Elpis this usually takes two hours. This build will only have to happen once. 

Open the `elpis-project/elpis` directory in VSCode.
 
To start the container, click the little green box in the bottom left-hand corner then select "Reopen in Container" or if you reopen the editor, a notification will pop up with the same option.

![Reopen in container](assets/dev-in-vscode/vsc-reopen-in-con.png)

Notice the little green box now specifies that the editor is open in a Docker container:

![VSCode in container](assets/dev-in-vscode/vsc-in-container.png)

## 6. Setup Python Development Environment

The `setup.py` file does all the hard work of installing linters and testing software which are listed in `requirements.txt`. Open a new terminal (from the menu select "Terminal > New Terminal") and run the following command to install Elpis' dependencies.  
`python setup.py develop`

### 6.1 Settings

In the root project directory, create a `.vscode` directory, in that create a `settings.json` file with the following contents:
```json
{
    "terminal.integrated.shell.linux": "/bin/zsh",
    "python.pythonPath": "/venv/bin/python3",
    "python.linting.pylintEnabled": true,
    "python.linting.pylintPath": "/venv/bin/pylint",
    "python.linting.enabled": true,
    "python.testing.pytestArgs": [],
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestEnabled": true
}
```

This will enable the Python extension, debugging, linting and unit testing facilities.

### 6.2 Run Config

Going one step further, we can setup some default run configurations so that when `F5` is pressed, the server is debuggable from within the editor. To crate a run config to start the server, in the `.vscode` directory, create a new file called `launch.json` with the following contents:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "elpis",
                "FLASK_ENV": "development",
                "FLASK_DEBUG": "0"
            },
            "args": [
                "run",
                "--host","0.0.0.0",
                "--port","5000",
                "--no-debugger",
                "--no-reload"
            ],
            "jinja": true
        }
    ]
}
```

Now press `F5` (or the play button) and see the server run. Try using breakpoints to pause the server at a line of code. Try the `elpis/elpis/__init__.py` file pause the program around line 72 on the print statement in the index function. To get the server to pause you will need to open a browser and load `0.0.0.0:5000/index.html` to run that section of code.

### 6.3 Terminal

Notice that when you press <code>ctrl+`</code> the terminal that opens is in the container.

## 7. Elpis-GUI

If you wish to develop the front end code along with the server, you can add an additional mount and override the `/elpis-gui` directory. Notice the second mount in the following code and replace `/path/to/elpis-gui` with the path to the `elpis-gui` git repository. If you followed the instructions for cloning the repository above your mount for the GUI should look like this `"type=bind,source=${localWorkspaceFolder}/../elpis-gui,target=/elpis-gui"`.

```json
{
    "name": "Elpis Dev Container (in progress)",
    "image": "coedl/elpis:latest",
    "workspaceFolder": "/elpis",
    "mounts": [
        "type=bind,source=${localWorkspaceFolder},target=/elpis",
        "type=bind,source=/path/to/elpis-gui,target=/elpis-gui"
    ],
	"settings": { 
		"terminal.integrated.shell.linux": "/bin/zsh",
		"python.pythonPath": "/venv/bin/python",
		"python.linting.pylintEnabled": true,
		"python.linting.pylintPath": "/venv/bin/pylint",
		"python.linting.enabled": true
	},
	"extensions": [
		"ms-python.python"
	]
}
```

### 7.1 Elpis-GUI w/ Hot-Reload

A more advanced method for developing the `elpis-gui` is to use the Webpack Dev Server's hot reload feature to automatically push your changes rather than waiting for `npm run watch` to pickup and then you having to force reload.

To use hot reload:

7.1.1. Update your `devcontainer.json` to include

```json
"forwardPorts": [
    3000, 
    5000
]
```

This will open port 5000 to access the Flask WSGI and port 3000 to access the Webpack Development Server.

It should look like this if you followed the previous examples:

```json
{
    "name": "Elpis Dev Container (in progress)",
    "image": "coedl/elpis:latest",
    "workspaceFolder": "/elpis",
    "mounts": [
        "type=bind,source=${localWorkspaceFolder},target=/elpis",
        "type=bind,source=/path/to/elpis-gui,target=/elpis-gui"
    ],
	"settings": { 
		"terminal.integrated.shell.linux": "/bin/zsh",
		"python.pythonPath": "/venv/bin/python3",
		"python.linting.pylintEnabled": true,
		"python.linting.pylintPath": "/venv/bin/pylint",
		"python.linting.enabled": true
	},
	"extensions": [
		"ms-python.python"
	],
    "forwardPorts": [
        3000, 
        5000
    ]
}
```


7.1.2. Update your `launch.json` to include the following as a launch configuration. Append it after the previous launch configuration.
```json
{
    "name": "Node: Elpis-Gui",
    "type": "node",
    "request": "launch",
    "cwd": "/elpis-gui/",
    "env": {
        "NODE_ENV": "development",
        "NODE_PATH": "src/",
        "WDS_SOCKET_PORT": "3000"
    },
    "runtimeExecutable": "npm",
    "runtimeArgs": ["start"],
    "console": "integratedTerminal"
}
```

You also need to set an additional environment variable for the Flask launch configuration. By setting `"WEBPACK_DEV_SERVER_PROXY": "True"` in `"env"` of the Flask configuration it will redirect front end requests to the webpack dev server. Your Flask launch config should look like this:

```json
{
    "name": "Python: Flask",
    "type": "python",
    "request": "launch",
    "module": "flask",
    "env": {
        "FLASK_APP": "elpis",
        "FLASK_ENV": "development",
        "FLASK_DEBUG": "0",
        "WEBPACK_DEV_SERVER_PROXY": "True"
    },
    "args": [
        "run",
        "--host","0.0.0.0",
        "--port","5000",
        "--no-debugger",
        "--no-reload"
    ],
    "jinja": true
}
```

7.1.3. To run both the webpack dev server and the flask server you need to click on the VSCode run/debug menu.

![Debug/Run Menu](assets/dev-in-vscode/debug-run-vscode.png)

Then select the `Node: Elpis GUI` from the launch drop down and hit the green arrow to run.

![Launch Selector](assets/dev-in-vscode/launch-selector.png)

You can then do the same for the `Python: Flask` server.

It will take some time for the GUI to be compiled, wait about a minute and then you can access the GUI by going to `127.0.0.0:5000`.

#### Caveats for hot-reload

* The Node configuration may take a while to start up. Wait for it... 
* Currently hot-reload does not preserve state #TODO
* Hot-reload can be buggy due to the flask intermediary, if you see a blank screen hard reload the page until the request succeeds.

## 8. Troubleshooting

If there are any problems with repositories being out of sync, the best thing to do is rebuild the dev Docker container from within VSCode. To do this, click the *Dev Container* option in the bottom left corner of VSCode or use the command pallet (cmd-shift-p) to find the `Remote-Containers: Rebuild container` and select it. This option will pull the newest elpis Docker image.

If there are further issues, check the `Dev Container` terminal (normally number 2.) (`ctrl-\``) for any errors that might have occurred while building the image.

## 9. End

Now you have an environment that is well connected within the container and can do all the following:

* Python linting
* degbugging with breakpoints and variable watching
* intelliSense
* unit testing
* Simple terminal access to the Docker container

The End.

## Download sample files

These are the complete files as used in this guide, set up for both Elpis and Elpis-GUI, with hot reloading.
* [devcontainer.js](assets/dev-in-vscode/devcontainer.json)
* [launch.json](assets/dev-in-vscode/launch.json)
* [settings.json](assets/dev-in-vscode/settings.json)

## References

1. [Visual Studio Code - Developing inside a Container](https://code.visualstudio.com/docs/remote/containers)
