"""
    pushlight-srv
    simple fastapi implementation for sqlite db access.
"""

import logging
import uvicorn

from fastapi import Depends, FastAPI, Request, status
# from fastapi import HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session

# from werkzeug.middleware.proxy_fix import ProxyFix

from utils import crud, models, schemas
from utils.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# app.wsgi_app = ProxyFix(app.wsgi_app, x_host=1)


# Dependency
def get_dbconn():
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
    """get root html; redirect to items/1 template test"""
    return RedirectResponse("/items/1")


@app.get("/items/{item_id}", response_class=HTMLResponse)
async def get_items(request: Request, item_id: str):
    """get item html for specific id"""
    return templates.TemplateResponse("template_item.html",
                                      {"request": request, "item_id": item_id})


@app.get("/items/last/{item_count}", response_class=HTMLResponse)
async def get_items_last(request: Request, item_count: int, dbconn: Session = Depends(get_dbconn)):
    """get item html for specific id"""
    lastitems = crud.get_lastgpsdata(dbconn=dbconn, item_count=item_count)
    # return templates.TemplateResponse("template_gpsdata.html",
    #                                   {"request": request, "lastitems": lastitems})
    return templates.TemplateResponse("template_gpsdata_tabulator.html",
                                      {"request": request, "lastitems": lastitems})


@app.post("/collect")
async def collect(pushlightdata: schemas.PushLightData, dbconn: Session = Depends(get_dbconn)):
    """append GPS data to persistent storage"""
    print(pushlightdata.json())
    crud.create_gpsdata(dbconn=dbconn, pushlightdata=pushlightdata)
    return


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """error handler for debug"""
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    # logging.error(f"{request}: {exc_str}")
    logging.error("%s: %s", request, exc_str)
    content = {'status_code': 10422, 'message': exc_str, 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8220)
