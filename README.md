
# Amarillo Continuous Deployment

Receiving [Github Webhooks](https://docs.github.com/en/developers/webhooks-and-events/webhooks/about-webhooks) in FastAPI to trigger updates.

All deployments of Amarillo use [gunicorn](https://gunicorn.org). 
Uvicorn is used for development with `--reload`.

## Running

Create a virtual environment, activate it and install dependencies
- `python3 -m venv venv`
- `. venv/bin/activate`
- `pip install -r requirements.txt`

Run `run.sh`.

## Amarillo-CD on itself

The idea is that commits to the `amarillo-cd` repo trigger updates 
to the running instance itself. 
For that the FastAPI process shuts itself down and is restarted in 
an infinite loop in `run.sh`.

Note: when `run.sh` is modified, the process needs to be started manually.