from datetime import datetime

from fastapi import FastAPI, Response
from pydantic import BaseModel


app = FastAPI(title="Server Time API", version="1.0.0")


class TimeResponse(BaseModel):
    server_time: datetime


@app.get("/time", response_model=TimeResponse)
async def get_server_time(response: Response) -> TimeResponse:
    """Return the current time in the server's local timezone."""
    response.headers["Cache-Control"] = "no-store"
    return TimeResponse(server_time=datetime.now().astimezone())
