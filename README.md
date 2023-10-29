# Converter

Convert anything form anywhere

## Development

This repo uses devcontainer for ease of use. For this to work you will need to install **docker** on your system. Docker is the only thing that is required to develop on this project.

After starting the dev container run:

```
make setup-dev
```

This will install the required packages needed for development

To start the dev servers run:

```
make dev
```

backend will be running on port **5000** and frontend will be running on port **8080**

For example, got to http://localhost:8080/ to see the frontend.

### Formating and linting

should be used before pushing to the repo.

```
make format
make lint
```

Development is possible without a dev container but it requires the coder to install dependencies themselves. (Make their own venv, install python packages, etc.)

---
