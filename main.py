import uvicorn
import sys
from fastapi import FastAPI, Body, Request
from datetime import datetime

print(f"Starting Amarillo-CD at {datetime.now().isoformat()}")

app = FastAPI()



@app.post("/payload")
async def root(payload: dict = Body(...)):
    is_amarillo_cd = payload.get('repository').get('name') == "amarillo-cd"

    if is_amarillo_cd:
        print(f"Exiting Amarillo-CD at {datetime.now().isoformat()}")
        sys.exit(0)

    is_main_branch = payload.get('ref') == 'refs/heads/main'
    if is_main_branch:
        print("Push to main")

    print(payload)

    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
