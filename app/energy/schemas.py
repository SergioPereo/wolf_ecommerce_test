from pydantic import BaseModel
from datetime import datetime

class Device(BaseModel):
    id: int
    device_name: str
    device_type: int
    device_status: int

class DeviceCreate(BaseModel):
    device_name: str
    device_type: int
    device_status: int

class DeviceStatusUpdate(BaseModel):
    device_status: int

class TypeForm(BaseModel):
    id: int

class DeviceType(BaseModel):
    id: int
    name: str
    
class DeviceTypeCreate(BaseModel):
    name: str

class Status(BaseModel):
    id: int
    name: str

class StatusCreate(BaseModel):
    name: str

class Reading(BaseModel):
    id: int
    device_id: int
    potence: float
    last_update: datetime

class ReadingCreate(BaseModel):
    device_id: int
    potence: float