import uvicorn
from fastapi import FastAPI, Body, Request

app = FastAPI()


@app.post("/payload")
async def root(payload: dict = Body(...)):
    is_main_branch = payload.get('ref') == 'refs/heads/main'
    if is_main_branch:
        print("Push to main")
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
