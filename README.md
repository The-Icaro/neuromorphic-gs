# neuromorphic-gs
Faculty Project - Neuromorphic Computing and Supercomputers

[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-31010/)
[![PEP20](https://img.shields.io/badge/code%20style-pep20-red.svg)](https://www.python.org/dev/peps/pep-0020/)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![bandit](https://img.shields.io/badge/code%20style-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Technology and Resources

- [Python 3.10](https://www.python.org/downloads/release/python-31010/) - **pre-requisite**
- [Docker](https://www.docker.com/get-started) - **pre-requisite**
- [Docker Compose](https://docs.docker.com/compose/) - **pre-requisite**
- [Pipenv](https://github.com/pypa/pipenv)
- [FastAPI](https://github.com/tiangolo/fastapi)
- [Uvicorn](https://github.com/encode/uvicorn)

_Please pay attention on **pre-requisites** resources that you must install/configure._

### API Docs

#### Routes

- `/`: The root path is a redirect to `/v1/docs`
- `/docs`: Swagger Docs
- `/redoc`: Redoc Docs
- `/v1/docs`: Swagger Docs V1
- `/v1/redoc`: Redoc Docs V1
- `/health-check`: Verify sure the application is up

## Running Docker

### How to Build Docker

```
make docker/build
```

### How to Run

```
make docker/run
```

### How to Test

```
make docker/test
```

### Recommended command to running the application

```
make docker/build && make docker/run
```

_The project will be running at `http://localhost:8000/`_

The `entrypoint` of this project is the `run.py` file on the root path.

This project needs Redis to be successful in its operation, when running the command `make docker/run` we will start Redis via docker-compose.

## Running locally
### How to Install

```
make local/install
```

### How to enter the virtual environment

```
make local/shell
```

### How to Run

```
make local/run
```

### How to Test
```
make local/test
```

### How to lint

`make docker/lint` or `make local/lint` to lint

`make docker/bandit` or `make local/bandit` to execute the bandit check

**Helpful commands**

_Please, check all available commands in the [Makefile](Makefile) for more information_.

## How to deploy

#### Kubernetes Deployment Quick Guide

This quick guide provides a summarized version of the steps to deploy your system on Kubernetes using the provided script and YAML files.

#### pre-requisites

- **Kubernetes Cluster:** Access to a Kubernetes cluster ([microK8s](https://microk8s.io/) assumed).

- **kubectl:** Installed and configured via [microk8s](https://microk8s.io/).