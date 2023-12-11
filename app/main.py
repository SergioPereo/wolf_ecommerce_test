from typing import Union, Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from .energy import crud, schemas, models
from .database import SessionLocal, engine

description = """
Devices monitoring tool
"""

app = FastAPI( description=description)

models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/devices/",response_model=list[schemas.Device])
def get_devices(skip: int = 0, limit: int = 100, 
               db: Session = Depends(get_db)
               ):
    return crud.get_devices(db, skip, limit)

@app.get("/devices/{device_id}", response_model=schemas.Device)
def get_devices_by_id(device_id: int, db: Session=Depends(get_db)):
    return crud.get_device_by_id(db, device_id)

@app.get("/devices/type/{device_type}", response_model=list[schemas.Device])
def get_devices_by_type(device_type: int, db: Session=Depends(get_db)):
    return crud.get_devices_by_type(db=db, type_id=device_type)

@app.get("/readings/", response_model=list[schemas.Reading])
def get_readings(skip: int = 0, limit: int = 100, db: Session=Depends(get_db)):
    return crud.get_readings(db, skip, limit)

@app.get("/readings/{device_id}", response_model=list[schemas.Reading])
def get_readings_by_device_id(device_id: int, db: Session=Depends(get_db)):
    return crud.get_readings_by_device_id(db, device_id)

@app.get("/readings/type/{device_type}", response_model=list[schemas.Reading])
def get_readings_by_device_id(device_type: int, db: Session=Depends(get_db)):
    return crud.get_readings_by_device_type(db, device_type)

@app.post("/devices/", response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate, db: Session=Depends(get_db)):
    return crud.create_device(db, device)

@app.post("/types/", response_model=schemas.DeviceType)
def create_type(type: schemas.DeviceTypeCreate, db: Session=Depends(get_db)):
    return crud.create_type(db, type)

@app.post("/statuses/", response_model=schemas.Status)
def create_status(status: schemas.StatusCreate, db: Session=Depends(get_db)):
    return crud.create_status(db, status)

@app.post("/readings/", response_model=schemas.Reading)
def create_reading(reading: schemas.ReadingCreate, db: Session=Depends(get_db)):
    return crud.create_reading(db, reading)

@app.put("/devices/update/{device_id}/", response_model=schemas.Device)
def update_device_status(device_id: int, device_status_update: schemas.DeviceStatusUpdate, db: Session=Depends(get_db)):
    return crud.update_device_status(db, device_id, device_status_update)