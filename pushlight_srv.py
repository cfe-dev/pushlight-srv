"""
    pushlight-srv
    simple fastapi implementation for sqlite db access.
"""

import uvicorn

from fastapi import Depends, FastAPI, Request
# from fastapi import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


@app.get("/", response_class=RedirectResponse)
def root():
    """get root html; redirect to /items/1/ template test"""
    return RedirectResponse("/items/1/")


@app.get("/items/{item_id}", response_class=HTMLResponse)
async def read_item(request: Request, item_id: str):
    """get item html for specific id"""
    return templates.TemplateResponse("template_item.html",
                                      {"request": request, "item_id": item_id})


@app.post("/collect")
async def collect(pushlightdata: schemas.PushLightData, dbconn: Session = Depends(get_db)):
    """append GPS data to persistent storage"""
    print(pushlightdata.json())
    crud.create_gpsdata(dbconn=dbconn, pushlightdata=pushlightdata)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8220)
