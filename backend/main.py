from typing import Union, Any
from fastapi import FastAPI, status
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


@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.post("/question")
def ask_question(question: Question, status_code=status.HTTP_200_OK):
    response = query_bot(question.question)
    return  {"response": response}
    




@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}