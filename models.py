"""pushlight-srv Database Models"""

from sqlalchemy import Column, Integer, String, Float
# from sqlalchemy import ForeignKey, Boolean
# from sqlalchemy.orm import relationship

from .database import Base


class GpsData(Base):
    """Flat Table for pushlight gps data points"""
    __tablename__ = "gpsdata"

    data_id = Column(Integer, primary_key=True, index=True)
    pushlight_client_id = Column(Integer, primary_key=True, index=True)
    sensor = Column(String, unique=True, index=True)
    lat = Column(Float)
    lon = Column(Float)
    age = Column(Integer)
    servo_angle = Column(Integer)
