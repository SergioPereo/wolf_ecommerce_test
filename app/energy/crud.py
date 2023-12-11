from sqlalchemy.orm import Session

from . import models,schemas
from fastapi import HTTPException
from datetime import datetime

def commit_model(db:Session, model: models.Base):
    db.add(model)
    db.commit()

def filter_reading_by_device_type(device_type: int):
    return models.Readings.devices.any(models.Devices.device_type == device_type)

def create_device(db: Session, device: schemas.DeviceCreate):
    if not get_type_by_id(db, type_id=device.device_type):
        raise HTTPException(status_code=400, detail="Ese tipo de dispositivo no existe")
    if not get_status_by_id(db, status_id=device.device_status):
        raise HTTPException(status_code=400, detail="Ese estado de dispositivo no existe")
    db_device = models.Devices(device_name=device.device_name, device_type=device.device_type, device_status=device.device_status)
    commit_model(db, db_device)
    db.refresh(db_device)
    return db_device

def create_status(db: Session, status: schemas.StatusCreate):
    db_status = models.Status(name=status.name)
    commit_model(db, db_status)
    db.refresh(db_status)
    return db_status

def create_type(db: Session, type: schemas.DeviceTypeCreate):
    db_type = models.DeviceTypes(name=type.name)
    commit_model(db, db_type)
    db.refresh(db_type)
    return db_type

def create_reading(db: Session, reading: schemas.ReadingCreate):
    device = get_device_by_id(db, device_id=reading.device_id)
    if reading.potence < 0:
        raise HTTPException(status_code=400, detail="No puede haber potencias negativas")
    if not device:
        raise HTTPException(status_code=400, detail="El dispositivo no existe")
    if device.status.name=="Mantenimiento":
        raise HTTPException(status_code=400, detail="El dispositivo no puede tener lecturas porque esta en mantenimiento")
    db_reading = models.Readings(device_id=reading.device_id, potence=reading.potence, last_update=datetime.now())
    commit_model(db, db_reading)
    db.refresh(db_reading)
    return db_reading

def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Devices).offset(skip).limit(limit).all()

def get_device_by_id(db: Session, device_id: int):
    return db.query(models.Devices).filter(models.Devices.id == device_id).first()

def get_devices_by_type(db: Session, type_id: int):
    return db.query(models.DeviceTypes).filter(models.DeviceTypes.id==type_id).first().devices

def get_readings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Readings).offset(skip).limit(limit).all()

def get_readings_by_device_id(db: Session, device_id: int):
    return db.query(models.Readings).filter(models.Readings.id == device_id)

def get_readings_by_device_type(db: Session, device_type: int):
    return db.query(models.Readings).filter(filter_reading_by_device_type(device_type)).all()

def get_status_by_id(db: Session, status_id: int):
    return db.query(models.Status).filter(models.Status.id == status_id).first()

def get_type_by_id(db: Session, type_id: int):
    return db.query(models.DeviceTypes).filter(models.DeviceTypes.id == type_id).first()

def update_device_status(db: Session, device_id: int, device_status_update: schemas.DeviceStatusUpdate):
    if not get_status_by_id(db, status_id=device_status_update.device_status):
        raise HTTPException(status_code=400, detail="Ese estado de dispositivo no existe")
    # This is not the right way to leave it. I must change the helpers method above to avoid using first as default
    # TODO: Change helpers and clean the line below
    device = db.query(models.Devices).filter(models.Devices.id == device_id)
    device.update({"device_status": device_status_update.device_status})
    db.commit()
    return device.first()