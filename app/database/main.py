from fastapi import Depends, FastAPI, HTTPException
from .database import session_local, engine
from . import models


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
        db = session_local()
        try :
                yield db
        finally:
                db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

