from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship

from app.database import Base

class DeviceTypes(Base):
    __tablename__ = "device_types"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)

    devices = relationship("Devices", back_populates="type")

class Status(Base):
    __tablename__ = "devices_status"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)

    devices = relationship("Devices", back_populates="status")

class Devices(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_name = Column(String, index=True)

    device_type = Column(Integer, ForeignKey("device_types.id"))
    device_status = Column(Integer, ForeignKey("devices_status.id"))

    type = relationship("DeviceTypes", back_populates="devices")
    status = relationship("Status", back_populates="devices")
    readings = relationship("Readings", back_populates="devices")

class Readings(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.id"))
    potence = Column(Float)
    last_update = Column(DateTime)

    devices = relationship("Devices", back_populates="readings")