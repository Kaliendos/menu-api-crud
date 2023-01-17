from fastapi import FastAPI

from menu import router


app = FastAPI()

app.include_router(router)
