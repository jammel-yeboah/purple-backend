# from fastapi import FastAPI
from api.endpoints import router  # Import your endpoint router
from fastapi import FastAPI
import uvicorn
import logging

app = FastAPI()
app.include_router(router)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup")
    for route in app.routes:
        logger.info(f"Route: {route.path} - {route.name}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)