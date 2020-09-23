# Developing in VSCode

Developing Elpis can be difficult at times as the software is run in a Docker container. This Docker container simplifies the installation of Elpis and its dependencies, but it also adds a barrier to quality development experience as the Python runtime and the code base are all on the container and not easily accessible on the local OS.

In the past, developers mounted volumes, exposed ports and ran commands in terminals connected to the docker image. With Elpis changing frequently, all these commands change as well and it is easy to lose track.

This tutorial aims to bring about the best possible development experience by setting up the VSCode editor to enable:
* Python linting
* Debugging with breakpoints and variable watching
* IntelliSense
* Unit testing
* Simple terminal access to the Docker container

This works by using VSCode extensions that install another layer on-top of the Elpis image that runs a VSCode server that allows the editor access to the Python runtime and seamless access to the container.

![s](assets/dev-in-vscode/architecture-containers.png)
(ref 1)

## 1. Install Docker and VSCode

Download VSCode ([Link](https://code.visualstudio.com/)).

Make a Docker account and download docker ([Link](https://hub.docker.com)).

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

1. `git clone https://github.com/CoEDL/elpis.git`

If you are planning on developing the Elpis GUI clone it as well.

2. `git clone https://github.com/CoEDL/elpis-gui.git`

Your final directory structure should look something like this with the two repositories side by side.

```
elpis-project
├── elpis
└── elpis-gui
```

NOTE: These setup instructions assume that you follow these instructions for cloning the repository.

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

## 5. Re-open VSCode in the Container

We are now ready to open the VSCode in the container. The first time this happens, Docker will need to build the container from the beginning. For Elpis this usually takes two hours. This build will only have to happen once. To start, click the little green box in the bottom left-hand corner then select "Reopen in Container" or if you reopen the editor, a notification will pop up with the same option.

![Reopen in container](assets/dev-in-vscode/vsc-reopen-in-con.png)

Notice the little green box now specifies that the editor is open in a docker container:

![VSCode in container](assets/dev-in-vscode/vsc-in-container.png)

## 6. Setup Python Development Environment

The `setup.py` does all the hard work of installing linters and testing software...

### 6.1 Install the Python Extension

Navigate to the extensions panel on the left bar once again and search for the Python extension. You'll notice that it must be installed again, but this time, it must be installed on the remote VSCode server. Click to install it. After installing, reload the editor (the install button will have turned into a blue reload button).

![Install Python](assets/dev-in-vscode/vsc-install-python.png)

### 6.2 Settings

In the root project directory, create a `.vscode` directory, in that crate a `settings.json` file with the following contents:
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

This will enable the python extension, debugging, linting and unit testing facilities.

### 6.3 Run Config

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

## 6.4 Terminal

Notice that when you press `ctrl-\`` the terminal that opens is in the container.

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

1. Update your `devcontainer.json` to include

```json
"forwardPorts": [
    3000, 
    5000
]
```

This will open port 5000 to access the Flask WSGI and port 3000 to access the Webpack Development Server.

It should look like this if you follow the previous examples:

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
	],
    "forwardPorts": [
        3000, 
        5000
    ]
}
```

Port 3000: Webpack Dev Server
Port 5000: Flask WSGI Server


2. Update your `launch.json` to include the following as a launch configuration. Append it after the previous launch configuration.
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
    "console": "integratedTerminal",
}
```

#### Caveats for hot-reload

* Currently hot-reload does not preserve state #TODO
* Hot-reload can be buggy due to the flask intermediary, just reload a couple times it'll get there

## 8. Troubleshooting

If there are any problems with repositories being out of sync, the best thing to do is rebuild the dev docker container from within VSCode. To do this, click the *Dev Container* option in the bottom left corner of VSCode or use the command pallet (cmd-shift-p) to find the `Remote-Containers: Rebuild container` and select it. This option will pull the newest elpis docker image.

If there are further issues, check the `Dev Container` terminal (normally number 2.) (`ctrl-\``) for any errors that might have occurred while building the image.

## 9. End

Now you have an environment that is well connected within the container and can do all the following:

* Python linting
* degbugging with breakpoints and variable watching
* intelliSense
* unit testing
* Simple terminal access to the Docker container

The End.

## References

1. [Visual Studio Code - Developing inside a Container](https://code.visualstudio.com/docs/remote/containers)
