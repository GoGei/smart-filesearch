from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, validator
from aitools.processors import AIToolProcessor

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="application/templates")

processor = AIToolProcessor()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class Question(BaseModel):
    user_query: str

    @validator("user_query")
    def validate_user_query(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("Question cannot be empty or whitespace")
        if len(value) >= 1024:
            raise ValueError("Question cannot be longer than 1024 characters")
        return value


class Answer(BaseModel):
    answer: str
    sources: str


@app.post("/ask/", response_model=Answer, responses={400: {"description": "OpenAI API raise an error"}})
async def ask(question: Question):
    user_query = question.user_query

    try:
        return processor.process(user_query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
