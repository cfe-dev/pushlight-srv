"""database access methods"""

# import datetime
from typing import List
from sqlalchemy.orm import Session

from .models import GpsData
from .schemas import PushLightData


def get_gpsdata(dbconn: Session, data_id: int) -> GpsData | None:
    """return a single data point by id"""
    return dbconn.query(GpsData).filter(
        GpsData.data_id == data_id).first()


def get_lastgpsdata(dbconn: Session, item_count: int, offset: int) -> List[GpsData]:
    """return last x data points by time"""
    # retval = dbconn.query(GpsData).order_by(
    #     GpsData.date.desc(), GpsData.time.desc()).limit(item_count)
    # retval = [GpsData(data_id=1, pushlight_client_id=2, sensor="gps"),
    #           GpsData(data_id=22, pushlight_client_id=33, sensor="gps")]
    retval = dbconn.query(GpsData).where(GpsData.data_id > offset).order_by(
        GpsData.data_id.desc()).limit(item_count)
    # retval = dbconn.query(GpsData).order_by(
    #     GpsData.data_id.desc()).limit(item_count)
    retval = retval[::-1]  # reverse
    return retval  # type: ignore


def create_gpsdata(dbconn: Session, pushlightdata: PushLightData):
    """append pushlight gps data points to db table"""
    for gpsdata in pushlightdata.gpsdata:

        # # reformat date int from ddmmyy to 20yymmdd
        # date_org: str = str(gpsdata.date)
        # date_tgt: str = ""
        # if len(date_org) == 6:
        #     date_tgt = "20" + \
        #         date_org[4] + date_org[5] + \
        #         date_org[2] + date_org[3] + \
        #         date_org[0] + date_org[1]
        # elif len(date_org) == 4:
        #     date_tgt = str(datetime.date.today().year) + \
        #         date_org[2] + date_org[3] + \
        #         date_org[0] + date_org[1]
        # else:
        #     date_tgt = datetime.date.today().strftime("%Y%m%d")

        # gpsdatetime = datetime.datetime(year=1, month=1, day=1, hour=1,
        #                                 minute=1, second=1, tzinfo=datetime.timezone.utc)

        gpsdata_model = GpsData(
            # data_id=1,
            pushlight_client_id=pushlightdata.pushlight_client_id,
            sensor=pushlightdata.sensor,
            lat=gpsdata.lat,
            lon=gpsdata.lon,
            age=gpsdata.age,
            # date=int(date_tgt),
            date=gpsdata.date,
            time=gpsdata.time,
            # datetime=gpsdatetime,
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
        # gpsdata.data_id = gpsdata_model["data_id"]
    # return pushlightdata
    return
