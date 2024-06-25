from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/facilities")
async def get_facilities():
    return {"facilities": "Hello Facilities"}


@app.get("/patients")
async def get_patients():
    return {"patients": "Hello Patients"}

@app.get("/auditors")
async def get_auditors():
    return {"auditors": "Hello Auditors"}



@app.get("/adrs")
async def get_patients():
    return {"adrs": "Hello adrs"}

@app.get("/stages")
async def get_patients():
    return {"stages": "Hello stages"}

@app.get("/submissions")
async def get_patients():
    return {"submissions": "Hello submissions"}

@app.get("/decisions")
async def get_patients():
    return {"decisions": "Hello decisions"}
