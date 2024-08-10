from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session
from Classes import *

app = FastAPI()

origins = [
  "*"
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

engine = create_engine("sqlite+pysqlite:///radr.db", echo=True)

def get_data(tablename, where="", orderby="", groupby="", limit=0):
  # Connect to DB and create a cursor
  DATABASE_URL = "radr.db"
  sqliteConnection = sqlite3.connect(DATABASE_URL)
  cursor = sqliteConnection.cursor()
  print('DB Init')

  querystr = (f'SELECT * FROM {tablename}')
  if where!="":
      querystr += f' WHERE {where}'
  if orderby!="":
      querystr += f' ORDER BY {orderby}'
  if groupby!="":
      querystr += f' GROUP BY {groupby}'
  if limit>0:
      querystr += f' LIMIT {limit}'
  res = cursor.execute(querystr).fetchall()

  cursor.close()
  sqliteConnection.close()
  
  keys = list(map(lambda x: x[0], cursor.description))
  
  data = {'data': [
    {keys[i]: r[i] for i in range(0, len(keys))} for r in res
  ]}
  
  return data


def query(table_name):
  tables = {
    "Facility": Facility,
    "Auditor": Auditor,
    "Patient": Patient,
    "Adr": Adr,
    "Stage": Stage,
    "Submission": Submission,
    "Decision": Decision,
    "Srn": Srn,
    "Dcn": Dcn,
  }
  with Session(engine) as session:
    stmt = select(tables[table_name])
    result = session.execute(stmt)
    
    data = []
    for row in result.all():
      data.append(row._mapping[table_name].as_dict())
    
    return {'data': data }
   

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/facilities")
async def get_facilities():
  data = query('Facility')
  return data


@app.get("/patients")
async def get_patients():
  data = query('Patient')
  return data

@app.get("/auditors")
async def get_auditors():
  data = query('Auditor')
  return data

@app.get("/adrs")
async def get_adrs():
  data = query('Adr')
  return data

@app.get("/stages")
async def get_stages():
  data = query('Stage')
  return data

@app.get("/submissions")
async def get_submissions():
  data = query('Submission')
  return data

@app.get("/decisions")
async def get_decisions():
  data = query('Decision')
  return data

@app.get("/srns")
async def get_srns():
  data = query('Srn')
  return data

@app.get("/dcns")
async def get_dcns():
  data = query('Dcn')
  return data

@app.get("/payments")
async def get_payments():
  data = query('Payment')
  return data
