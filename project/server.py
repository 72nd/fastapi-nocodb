from .log import logger
from .model import NocoCourses, NocoPersons

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from nocodb.exceptions import NocoDBAPIError


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html.jinja2", {"request": request})


@app.get("/api/course")
async def get_courses():
    try:
        data = NocoCourses.from_nocodb()
    except NocoDBAPIError as e:
        message = f"NocoDBAPIError. Message: {e}. Response Text: {e.response_text}"
        logger.error(message)
        raise HTTPException(status_code=500, detail=message)
    return data.model_dump()



@app.get("/api/person")
async def get_persons():
    try:
        data = NocoPersons.from_nocodb()
    except NocoDBAPIError as e:
        message = f"NocoDBAPIError. Message: {e}. Response Text: {e.response_text}"
        logger.error(message)
        raise HTTPException(status_code=500, detail=message)
    return data.model_dump()