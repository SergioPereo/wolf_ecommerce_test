from pydantic import BaseModel
from datetime import datetime

class Device(BaseModel):
    id: int
    device_name: str
    device_type: int
    device_status: int


class DeviceType(BaseModel):
    id: int
    name: str


class Status(BaseModel):
    id: int
    device_name: str
    device_type: int
    device_status: int


class Reading(BaseModel):
    id: int
    device_id: int
    potence: float
    last_update: datetime