"""
    pushlight-srv
    simple fastapi implementation for sqlite db access.
"""

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    """get root html"""
    a_val = "a"
    b_val = "b" + a_val
    return {"hello world": b_val}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8220)
