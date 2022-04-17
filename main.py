import sys
from fastapi import FastAPI, Body, Request
from datetime import datetime
from util import guvicorn_process, is_amarillo_cd
import signal

print(f"Starting Amarillo-CD at {datetime.now().isoformat()}")

app = FastAPI()


@app.post("/payload")
async def root(payload: dict = Body(...)):
    if await is_amarillo_cd(payload):
        print(f"Sending SIGTERM to Amarillo-CD at {datetime.now().isoformat()}.")

        # https://docs.gunicorn.org/en/stable/signals.html
        guvicorn_process().send_signal(signal.SIGTERM)

        return

    is_main_branch = payload.get('ref') == 'refs/heads/main'
    if is_main_branch:
        print("Push to main")

    print(payload)

    return {"message": "OK"}

