"""database access methods"""

from typing import List
from sqlalchemy.orm import Session

from .models import GpsData
from .schemas import PushLightData


def get_gpsdata(dbconn: Session, data_id: int) -> GpsData | None:
    """return a single data point by id"""
    return dbconn.query(GpsData).filter(
        GpsData.data_id == data_id).first()


def get_lastgpsdata(dbconn: Session, item_count: int) -> List[GpsData]:
    """return last x data points by time"""
    retval = dbconn.query(GpsData).order_by(
        GpsData.date.desc(), GpsData.time.desc()).limit(item_count)
    # retval = [models.GpsData(data_id=1, pushlight_client_id=2, sensor="gps"),
    #           models.GpsData(data_id=22, pushlight_client_id=33, sensor="gps")]
    retval = retval[::-1]  # reverse
    return retval


def create_gpsdata(dbconn: Session, pushlightdata: PushLightData):
    """append pushlight gps data points to db table"""
    for gpsdata in pushlightdata.gpsdata:
        gpsdata_model = GpsData(
            # data_id=1,
            pushlight_client_id=pushlightdata.pushlight_client_id,
            sensor=pushlightdata.sensor,
            lat=gpsdata.lat,
            lon=gpsdata.lon,
            age=gpsdata.age,
            date=gpsdata.date,
            time=gpsdata.time,
            altitude=gpsdata.altitude,
            course=gpsdata.course,
            speed_kmph=gpsdata.speed_kmph,
            servo_angle=gpsdata.servo_angle)
        # gpsdata_model = models.GpsData(**gpsdata.dict(),
        #                                pushlight_client_id=pushlightdata.pushlight_client_id,
        #                                sensor=pushlightdata.sensor)
        dbconn.add(gpsdata_model)
        dbconn.commit()
        dbconn.refresh(gpsdata_model)
        gpsdata.data_id = gpsdata_model["data_id"]
    return pushlightdata
