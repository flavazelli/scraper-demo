from fastapi import FastAPI, status
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import time
import atexit
from pydantic import BaseModel
from langchain_chain import query_bot
from fastapi.middleware.cors import CORSMiddleware

class Question(BaseModel):
    question: str

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
    response = query_bot(question.question)
    return  {"response": response}