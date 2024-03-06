# This repository mirrors the real repository from GitLab

# Converter

Convert anything form anywhere

## Development

To develop on this project you have 2 options:

1) use VSCode **dev container** (preffered)
2) use your **own** environment

### VSCode dev container
Using a dev container you dont need to setup anything on your own. All the **helpful extentions** are installed for you, all the **dependencies** are installed for you, and you can **start developing right away**.

Before you start developing in a dev container you will need to install 2 things on your system:

1) [Docker](https://docs.docker.com/get-docker/)
2) [VSCode](https://code.visualstudio.com/download)

NB! After you have installed Docker you **dont need to do anything with it**. VSCode will use it for you.

After you have installed Docker and VSCode you can start developing in a dev container:

1) Clone this repo:
In your terminal run:
```
git clone https://gitlab.cs.taltech.ee/ririvi/iti0105-2023.git
```
2) Open the project in VSCode:
```
cd iti0105-2023
code .
```

3) Click the **blue button** in the bottom left corner of VSCode (open in remote window):

![alt](./README-assets/remote-windows-button.png)


4) After clicking it you will see a popup. Click **"Reopen in Container"**

5) Wait for the container to build and you are ready to go! (it can take several minutes when you open the project for the first time).

6) useful commands are available in the **makefile**. You can run them in the **terminal** in VSCode. Commands are listed below.

### Your own environment
If you dont want to use a dev container you can setup your own environment. If you choose this route you will need to install all the dependencies yourself and you will need to install all the helpful extentions yourself.



## Usage

### start web server
```
make web-dev
```

### start backend
```
make server-dev
```

### install dependencies
```
make install
```


# Used technologies

## Project management
- [git](https://git-scm.com/)
- [gitlab](https://about.gitlab.com/)
- [dev containers](https://code.visualstudio.com/docs/remote/containers)
- [makefile](https://www.gnu.org/software/make/manual/make.html)
- [markdown](https://www.markdownguide.org/)
- [docker](https://www.docker.com/)
- [VSCode](https://code.visualstudio.com/)

## Frontend
- [html, css, js](https://www.w3schools.com/)
- [prettier](https://prettier.io/)
- [GitLab pages](https://docs.gitlab.com/ee/user/project/pages/)

## Backend
- [python](https://www.python.org/)
- [flask](https://flask.palletsprojects.com/en/2.0.x/)
- [sqlite](https://www.sqlite.org/index.html)
- yt-dlp
- [JWT](https://jwt.io/)
- [bcrypt](https://pypi.org/project/bcrypt/)

