# Installing Elpis with Docker

Elpis can be installed with Docker, a virtual computer running on **your** computer. To use this version of Elpis, you first need to install Docker.


Docker is a program which helps standardise the way we do computational tasks with data, regardless of the operating systems of all the people who might want to run those tasks. Rather than building separate code for Windows, Linux, Mac operating systems, we can write once and run it on a myriad of operating systems using Docker. For more information about Docker, view [Nay San's slides](http://goo.gl/qxQDPP).

[Follow the instructions on the Docker site to install Docker.](https://www.docker.com/products/docker-desktop)
You will need to create a (free) account with them to be able to download the Docker installer.


After you have installed Docker, start it. On a Mac, you will see a little whale icon in the top menu bar. On Windows you'll see a whale icon in the system tray.

With Docker running, we will use a **terminal** to install Elpis.

 > When you use an application like Elan or Word, you are using a 'graphical user interface (GUI)' to do stuff to your data via menus and buttons. Another way of interacting with your computer is via a terminal, also known as a command line or command prompt.

On Mac, open the *Terminal* app in your *Applications > Utilities* folder.

For Windows, open the search field in your taskbar, type  `command` or `cmd` into it. Then, click or tap on the *Command Prompt* result to open it.

Download and run the Elpis Docker image by pasting this command in a terminal and pressing `Return` (or `Enter`).

```
docker run --rm -p 5000:5000/tcp coedl/elpis:latest
```

![Docker run](assets/elpis-workshop-with-docker/command-1-online.png)


When you see a message about the server running, open `http://0.0.0.0:5000` in a browser.

![Docker run](assets/elpis-workshop-with-docker/command-2-online.png)


You should see the Elpis interface.

![Docker run](assets/elpis-workshop-with-docker/10-welcome.png)


With Elpis going, follow the steps in the [Elpis online workshop](elpis-workshop.html).

