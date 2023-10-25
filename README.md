# Converter

Convert anything form anywhere

---

## Development

This repo uses devcontainer for ease of use. For this to work you will need to install **docker** on your system. Docker is the only thing that is required to develop on this project.

After starting the dev container run:

```
make setup-dev
```

This will install the required packages needed for development.

### Development server

To start the development server run:

```
make server-dev
```

After running the command the server will be available at `localhost:5000`.
### Formating and linting
should be used before pushing to the repo.

```
make format
make lint
```

Development is possible without a dev container but it requires the coder to install dependencies themselves. (Make their own venv, install node etc)

---
