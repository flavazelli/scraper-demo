from fastapi import FastAPI, status
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time
import atexit
from pydantic import BaseModel
from langchain_chain import query_bot
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile
from typing import Union
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import base64

class Question(BaseModel):
    question: Union[str, None]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)
scheduler = BackgroundScheduler()

#TODO: refactor scraper so they can launch once a day

def print_time():
    print(f"The current time is {time.ctime()}")

scheduler.add_job(print_time, CronTrigger(minute="*/1")) 
scheduler.start()

@atexit.register
def shutdown():
    scheduler.shutdown()


@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {"status" : "ok"}

@app.post("/question")
def ask_question(question: Question, status_code=status.HTTP_200_OK):
    if question.question:
        response = query_bot(question.question)
        return {"response": response}

@app.post("/file")
def ask_question(file: UploadFile, status_code=status.HTTP_200_OK):
    image_data = base64.b64encode(file.file.read()).decode('utf-8')
    model = ChatOpenAI(model="gpt-4o-mini")
    message = HumanMessage(
        content=[
            {"type": "text", "text": "extract each item from this grocery list into a comma separated list"},
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
            },
        ],
    )

    extractList = model.invoke([message])
    response =  query_bot(extractList.content)
    return {"response": response}
