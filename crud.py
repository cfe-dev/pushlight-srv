"""database access methods"""

from sqlalchemy.orm import Session

from . import models, schemas


def get_gpsdata(dbconn: Session, data_id: int):
    """return a single data point by id"""
    return dbconn.query(models.GpsData).filter(models.GpsData.data_id == data_id).first()


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
        dbconn.add(gpsdata_model)
        dbconn.commit()
      # dbconn.refresh(gpsdata)
    return True
