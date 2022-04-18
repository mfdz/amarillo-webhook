from fastapi import FastAPI, Body
from util import guvicorn_process, is_amarillo_cd
import signal
import logging

logger = logging.getLogger(__name__)

logger.info(f"CD started.")

app = FastAPI()


@app.post("/payload")
async def payload(payload: dict = Body(...)):
    if await is_amarillo_cd(payload):
        logger.info(f"CD sending SIGTERM to itself.")

        # https://docs.gunicorn.org/en/stable/signals.html
        guvicorn_process().send_signal(signal.SIGTERM)

        return

    is_main_branch = payload.get('ref') == 'refs/heads/main'
    if is_main_branch:
        logger.info(f"CD sending SIGTERM to amarillo-dev.")
        guvicorn_process(process_name="amarillo-dev").send_signal(signal.SIGTERM)
        return

    is_release_branch = payload.get('ref') == 'refs/heads/release'
    if is_release_branch:
        logger.info(f"CD sending SIGTERM to amarillo-prod.")
        guvicorn_process(process_name="amarillo-prod").send_signal(signal.SIGTERM)
        return

    print(payload)
