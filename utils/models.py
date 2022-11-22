"""pushlight-srv Database Models"""

from sqlalchemy import Column, Integer, String, Float
# from sqlalchemy import ForeignKey, Boolean
# from sqlalchemy.orm import relationship

from .database import Base


class GpsData(Base):
    """Flat Table for pushlight gps data points"""
    __tablename__ = "gpsdata"

    data_id = Column(Integer, primary_key=True)
    pushlight_client_id = Column(Integer, index=True)
    # sensor = Column(String, unique=True, index=True)
    sensor = Column(String, index=True)
    lat = Column(Float)
    lon = Column(Float)
    age = Column(Integer)
    date = Column(Integer)
    time = Column(Integer)
    altitude = Column(Float)
    course = Column(Float)
    speed_kmph = Column(Float)
    servo_angle = Column(Integer)
