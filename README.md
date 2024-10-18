[![tests](https://github.com/laaraujo/medical-spa-api/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/laaraujo/medical-spa-api/actions/workflows/tests.yml)
[![build](https://github.com/laaraujo/medical-spa-api/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/laaraujo/medical-spa-api/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/laaraujo/medical-spa-api/graph/badge.svg?token=aRjRfsGQeg)](https://codecov.io/gh/laaraujo/medical-spa-api)

# Medical Spa API

## Local setup

```sh
git clone git@github.com:laaraujo/medical-spa-api.git # clone this repo
cd medical-spa-api # cd into repository directory
python -m venv .venv # create virtual environment
source .venv/bin/activate # activate virtual environment
pip install -r requirements.txt # install dependencies
pre-commit install # initialize pre-commit hooks
cp .env.example .env # create .env file
make build # build containers
make run # run your containers locally
```

## Testing

The following command should be all you need (while in the root folder of this repo):

```
make test
```

- Keep in mind we are mostly running api endpoint tests so make sure to have the database running (`make run`) in another shell instance

## Make commands

```
build .................... : Build local containers
run ...................... : Run local containers
stop ..................... : Stop local containers
down ..................... : Stop and delete local container
makemigrations ........... : Django makemigrations command
migrate .................. : Django migrate command
createsuperuser .......... : Django createsuperuser command
shell .................... : Django shell command
collectstatic ............ : Django collectstatic command
sh ....................... : SSH into local API container
linter ................... : Run Ruff linter against all files in this repo
test ..................... : Run automated tests
```

## Documentation

Swagger docs are available in the `/docs/` endpoint (http://localhost:8000/docs/).

## Tech Features

- [Makefile](./Makefile) for better local dev experience
- [Djoser](https://djoser.readthedocs.io/) for authentication
- [Whitenoise](https://whitenoise.readthedocs.io/) for serving static files (docs and admin)
- [Docker](https://www.docker.com/) and [Compose](https://docs.docker.com/compose/) for development and production containers
- [PostgreSQL](https://www.postgresql.org/) database
- [DRF Spectacular](https://drf-spectacular.readthedocs.io/) for documentation
- Pre-commit hooks w/ [Ruff](https://docs.astral.sh/ruff/) linter and [OTB Pre-commit hooks](https://github.com/pre-commit/pre-commit-hooks)
- [Pytest](https://docs.pytest.org/) for testing
