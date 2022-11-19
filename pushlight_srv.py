"""
    pushlight-srv
    simple fastapi implementation for sqlite db access.
"""

import uvicorn

from fastapi import APIRouter, Depends, FastAPI, Request
# from fastapi import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from utils import crud, models, schemas
from utils.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# app = FastAPI(root_path='/pushlight_srv/v1')
# app = FastAPI(root_path='/pushlight_srv')
app = FastAPI()

prefix_router = APIRouter(prefix="/pushlight_srv/v1")


# Dependency
def get_db():
    """open db connection"""
    dbconn = SessionLocal()
    try:
        yield dbconn
    finally:
        dbconn.close()


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@prefix_router.get("/", response_class=RedirectResponse)
def root():
    """get root html; redirect to items/1 template test"""
    return RedirectResponse("items/1")


@prefix_router.get("/items/{item_id}", response_class=HTMLResponse)
async def read_item(request: Request, item_id: str):
    """get item html for specific id"""
    return templates.TemplateResponse("template_item.html",
                                      {"request": request, "item_id": item_id})


@prefix_router.get("/items/last/{item_count}", response_class=HTMLResponse)
async def read_lastitems(request: Request, item_count: int, dbconn: Session = Depends(get_db)):
    """get item html for specific id"""
    lastitems = crud.get_lastgpsdata(dbconn=dbconn, item_count=item_count)
    return templates.TemplateResponse("template_gpsdata.html",
                                      {"request": request, "lastitems": lastitems})


@prefix_router.post("/collect")
async def collect(pushlightdata: schemas.PushLightData, dbconn: Session = Depends(get_db)):
    """append GPS data to persistent storage"""
    print(pushlightdata.json())
    crud.create_gpsdata(dbconn=dbconn, pushlightdata=pushlightdata)


app.include_router(prefix_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8220)
