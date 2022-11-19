"""database access methods"""

from typing import List
from sqlalchemy.orm import Session

from . import models, schemas


def get_gpsdata(dbconn: Session, data_id: int) -> models.GpsData:
    """return a single data point by id"""
    return dbconn.query(models.GpsData).filter(
        models.GpsData.data_id == data_id).first()


def get_lastgpsdata(dbconn: Session, item_count: int) -> List[models.GpsData]:
    """return last x data points by time"""
    retval = dbconn.query(models.GpsData).order_by(
        models.GpsData.age.desc()).limit(item_count)
    # retval = [models.GpsData(data_id=1, pushlight_client_id=2, sensor="gps"),
    #           models.GpsData(data_id=22, pushlight_client_id=33, sensor="gps")]
    retval = retval[::-1]  # reverse
    return retval


def create_gpsdata(dbconn: Session, pushlightdata: schemas.PushLightData):
    """append pushlight gps data points to db table"""
    for gpsdata in pushlightdata.gpsdata:
        gpsdata_model = models.GpsData(
            # data_id=1,
            pushlight_client_id=pushlightdata.pushlight_client_id,
            sensor=pushlightdata.sensor,
            lat=gpsdata.lat,
            lon=gpsdata.lon,
            age=gpsdata.age,
            servo_angle=gpsdata.servo_angle)
        # gpsdata_model = models.GpsData(**gpsdata.dict(),
        #                                pushlight_client_id=pushlightdata.pushlight_client_id,
        #                                sensor=pushlightdata.sensor)
        dbconn.add(gpsdata_model)
        dbconn.commit()
        dbconn.refresh(gpsdata_model)
        gpsdata.data_id = gpsdata_model.data_id
    return pushlightdata
