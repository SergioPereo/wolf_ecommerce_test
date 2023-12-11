from sqlalchemy.orm import Session

from . import models,schemas
from fastapi import HTTPException
import hashlib

def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Devices).offset(skip).limit(limit).all()