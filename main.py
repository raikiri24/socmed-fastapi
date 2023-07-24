from fastapi import FastAPI, Depends
from models import all_models
from configs.db import engine
from routes import auth, posts


def create_app():
    app = FastAPI()

    all_models.Base.metadata.create_all(bind=engine)

    app.include_router(auth.router)
    app.include_router(posts.router)

    return app


app = create_app()
