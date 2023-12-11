from typing import Union, Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .energy import crud, schemas, models
from .database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/devices/",response_model=list[schemas.Device])
def get_devices(skip: int = 0, limit: int = 100, 
               db: Session = Depends(get_db)
               ):
    return crud.get_devices(db, skip, limit)