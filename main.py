from fastapi import FastAPI
import sqlite3
import json
from sqlalchemy import create_engine, text, select
from sqlalchemy.orm import Session
from Classes import *

app = FastAPI()

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
  print(res)
  
  data = {'data': [
    {keys[i]: r[i] for i in range(0, len(keys))} for r in res
  ]}
  
  return data

def query_adrs(args):
  with Session(engine) as session:
    # stmt = text("SELECT * FROM adr")
    stmt = select(Adr)
    result = session.execute(stmt)
    print("R:", result)

    data = []
    for row in result:
       data.append(f"adr_id: {row.adr_id}")

    
    data
    return data


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/facilities")
async def get_facilities():
  data = get_data('facility')
  return data


@app.get("/patients")
async def get_patients():
  data = get_data('patient')
  return data

@app.get("/auditors")
async def get_auditors():
  data = get_data('auditor')
  return data

@app.get("/adrs")
async def get_adrs():
  data = query_adrs('adr')
  return data

@app.get("/stages")
async def get_stages():
  data = get_data('stage')
  return data

@app.get("/submissions")
async def get_submissions():
  data = get_data('submission')
  return data

@app.get("/decisions")
async def get_decisions():
  data = get_data('decision')
  return data

@app.get("/srns")
async def get_srns():
  data = get_data('srn')
  return data

@app.get("/dcns")
async def get_dcns():
  data = get_data('dcn')
  return data

@app.get("/payments")
async def get_payments():
  data = get_data('payment')
  return data
