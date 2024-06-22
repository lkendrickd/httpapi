from fastapi import FastAPI
from prometheus_client import start_http_server, Summary
import logging
import time

from middleware import setup_middlewares
from error_handlers import setup_error_handlers

app = FastAPI()
setup_middlewares(app)
setup_error_handlers(app)

REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/metrics")
async def metrics():
    return app.state.metrics

@app.get("/")
@REQUEST_TIME.time()
async def root():
    return {"message": "Hello from httpapi"}

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    start_http_server(8000)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
