from fastapi import FastAPI
from fastapi.requests import Request
import time
import logging

logger = logging.getLogger("uvicorn.access")
logger.disabled = True

def register_middleware(app: FastAPI):
    
    @app.middleware("http")
    async def logging(request: Request, next):
        start_time = time.time()        

        response = await next(request)

        processing_time = time.time() - start_time

        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {processing_time}s"

        print(message)

        return response
