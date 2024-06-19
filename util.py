import psutil
import subprocess
import logging

logger = logging.getLogger(__name__)

def gunicorn_process(process_name: str = "amarillo-cd", kind: str = "master"):
    """Get the gunicorn process

    Gunicorn must be started with `--name` and will be displayed like
    name='gunicorn: worker [amarillo-cd]' with `ps`.
    """
    processes = [p for p in psutil.process_iter(['name', 'exe', 'cmdline'])
                 if p.name() == f'gunicorn: {kind} [{process_name}]']

    assert len(processes) <= 1, f"There should not be more than one process with name {process_name} and kind {kind}."

    return processes[0] if processes else None


async def is_amarillo_cd(payload):
    return payload.get('repository').get('name') == "amarillo-webhook"


def run_command(command):
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        if result.stderr:
            logger.error(f"Error: {result.stderr.decode('utf-8')}")
        raise subprocess.CalledProcessError(
                returncode = result.returncode,
                cmd = result.args,
                stderr = result.stderr
                )
    if result.stdout:
        logger.info(result.stdout.decode('utf-8'))
    return result