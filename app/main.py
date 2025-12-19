import uvicorn
from fastapi import FastAPI
from app.routers.api import api_router


app = FastAPI()

@app.get("/")
def hello():
    return "hello, world!"

app.include_router(api_router)
