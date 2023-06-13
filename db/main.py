from fastapi import FastAPI
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Base

app = FastAPI()

# Dependency to get a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def create_database():
    Base.metadata.create_all(bind=engine)

# Define your routes and database operations here
