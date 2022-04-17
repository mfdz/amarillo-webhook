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
        print(f"Exiting Amarillo-CD at {datetime.now().isoformat()}")
        guvicorn_process().send_signal(signal.SIGTERM)

        # not sure if this response is sent or the SIGTERM is faster
        return {"message": "Restarting Amarillo-CD"}

    is_main_branch = payload.get('ref') == 'refs/heads/main'
    if is_main_branch:
        print("Push to main")

    print(payload)

    return {"message": "OK"}

