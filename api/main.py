# from fastapi import FastAPI
from api.endpoints import router  # Import your endpoint router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)
