from datetime import date, datetime

from fastapi import FastAPI, Response
from pydantic import BaseModel


app = FastAPI(title="Server Time API", version="1.0.0")


class TimeResponse(BaseModel):
    server_time: datetime


class DateResponse(BaseModel):
    server_date: date


class YearResponse(BaseModel):
    year: int


class MonthResponse(BaseModel):
    month: int


class DayResponse(BaseModel):
    day: int


@app.get("/time", response_model=TimeResponse)
async def get_server_time(response: Response) -> TimeResponse:
    """Return the current time in the server's local timezone."""
    response.headers["Cache-Control"] = "no-store"
    return TimeResponse(server_time=datetime.now().astimezone())


@app.get("/date", response_model=DateResponse)
async def get_server_date(response: Response) -> DateResponse:
    """Return the current date in the server's local timezone."""
    response.headers["Cache-Control"] = "no-store"
    return DateResponse(server_date=datetime.now().astimezone().date())


@app.get("/date/year", response_model=YearResponse)
async def get_server_year(response: Response) -> YearResponse:
    """Return the current year in the server's local timezone."""
    response.headers["Cache-Control"] = "no-store"
    return YearResponse(year=datetime.now().astimezone().year)


@app.get("/date/month", response_model=MonthResponse)
async def get_server_month(response: Response) -> MonthResponse:
    """Return the current month in the server's local timezone."""
    response.headers["Cache-Control"] = "no-store"
    return MonthResponse(month=datetime.now().astimezone().month)


@app.get("/date/day", response_model=DayResponse)
async def get_server_day(response: Response) -> DayResponse:
    """Return the current day of the month in the server's local timezone."""
    response.headers["Cache-Control"] = "no-store"
    return DayResponse(day=datetime.now().astimezone().day)
