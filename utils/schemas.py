"""pushlight-srv json Schemas"""

from typing import List
from pydantic import BaseModel


class GpsData(BaseModel):
    """gpsdata line"""
    data_id: int
    lat: float
    lon: float
    age: int
    date: int
    time: int
    altitude: float
    course: float
    speed_kmph: float
    servo_angle: int

    class Config:
        """access members directly"""
        orm_mode = True


class PushLightData(BaseModel):
    """/collect endpoint json"""
    pushlight_client_id: int
    sensor: str
    gpsdata: List[GpsData]

    class Config:
        """access members directly"""
        orm_mode = True
