from pydantic import BaseModel
from fastapi import FastAPI
class User(BaseModel):
    username: str
    password: str
app=FastAPI()
@app.post("/login/")
def login(user: User):
    return {"username": user.username}

