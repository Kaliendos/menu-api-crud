from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI

from menu import router

app = FastAPI()
app.add_middleware(
    DebugToolbarMiddleware,
    panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
    session_generators=["config.database.db:get_session"]
)
app.include_router(router)




