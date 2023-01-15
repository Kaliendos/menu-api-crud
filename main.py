from fastapi import FastAPI
from debug_toolbar.middleware import DebugToolbarMiddleware


from menu import router


app = FastAPI(debug=True)
app.add_middleware(
    DebugToolbarMiddleware,
    panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
    session_generators=["config.database.db:get_session"]
)
app.include_router(router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


