import uvicorn
from fastapi import FastAPI
from app.routers.api import api_router

# Ensure models are imported and registered before the app starts
import app.models  # registers ORM models in correct order

app = FastAPI()

app.include_router(api_router)
