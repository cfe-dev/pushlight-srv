"""
    pushlight-srv
    simple fastapi implementation for sqlite db access.
"""

import uvicorn

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel


class GpsData(BaseModel):
    """/collect endpoint json"""
    lat: float
    lon: float
    age: int
    servo_angle = int


app = FastAPI()

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
async def collect(gpsdata: GpsData):
    """append GPS data to persistent storage"""
    # TODO read json & save
    print(gpsdata.json())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8220)
