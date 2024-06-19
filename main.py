from fastapi import FastAPI, Body, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from util import gunicorn_process, is_amarillo_cd, run_command
import signal
import logging
import docker
import uvicorn
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    dev_compose_folder: str

config = Config(_env_file='.env', _env_file_encoding='utf-8')

logging.basicConfig(
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logger = logging.getLogger(__name__)

logger.info(f"CD started.")

docker_client = docker.from_env()

app = FastAPI()

security = HTTPBasic()

@app.post("/payload")
async def payload(payload: dict = Body(...)):
    if await is_amarillo_cd(payload):
        logger.warning(f"CD sending SIGTERM to itself.")

        # https://docs.gunicorn.org/en/stable/signals.html
        gunicorn_process().send_signal(signal.SIGTERM)

        return

    is_main_branch = payload.get('ref') == 'refs/heads/main'
    if is_main_branch:
        logger.warning(("CD trying to stpp the amarillo-dev container"))

        container = docker_client.containers.get("amarillo-dev")
        logger.warning((f"CD stopping container {container}"))

        container.stop()
        logger.warning((f"CD container stopped"))

        #logger.warning(f"CD sending SIGTERM to amarillo-dev.")
        #gunicorn_process(process_name="amarillo-dev").send_signal(signal.SIGTERM)
        return

    is_release_branch = payload.get('ref') == 'refs/heads/release'
    if is_release_branch:
        logger.warning(f"CD sending SIGTERM to amarillo-prod.")
        gunicorn_process(process_name="amarillo-prod").send_signal(signal.SIGTERM)
        return

    print(payload)

def verify_secret(credentials: HTTPBasicCredentials = Depends(security)):
    with open('secret.txt', 'r') as secret_file:
        secret = secret_file.read().strip()
        if credentials.password != secret:
            raise HTTPException(status_code=401, detail="Incorrect deploy secret")

@app.post("/mitanand")
async def payload_mitanand(payload: dict = Body(...), security = Depends(verify_secret)):
    logger.warning(("CD trying to stop the amarillo-mitanand container"))

    container = docker_client.containers.get("amarillo-mitanand")
    logger.warning((f"CD stopping container {container}"))

    container.stop()
    logger.warning((f"CD container stopped"))

@app.post("/dev")
async def payload_dev(payload: dict = Body(...), security = Depends(verify_secret)):
    project_name = "dev"
    compose_folder = config.dev_compose_folder
    env_file_path = f"{compose_folder}/dev.env"

    logger.info(f"Running pull command for {project_name}")
    pull_command = f"docker compose -f {compose_folder}/compose.yaml --env-file {env_file_path} --profile enhancer --profile generator pull"
    run_command(pull_command)

    logger.info(f"Running up command for {project_name}")
    up_command = f"docker compose -f {compose_folder}/compose.yaml --env-file {env_file_path} --profile enhancer --profile generator -p {project_name} up -d"
    run_command(up_command)

    logger.info(f"CD ran for {project_name}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
