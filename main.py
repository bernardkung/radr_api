from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
import pandas as pd
from sqlalchemy import create_engine, text, select, func
from sqlalchemy.orm import Session
from Classes import *

app = FastAPI()


## Engine configuration
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


## Extra Configuration
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


## Function Definition
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

  with Session(engine) as session:
    stmt = select(tables[table_name])
    result = session.execute(stmt)
    
    data = []
    for row in result.all():
      data.append(row._mapping[table_name].as_dict())
    
    return {'data': data }
  
def full_query(args):
   with Session(engine) as session:
      stmt = (
        select(
          Adr, 
          Facility, 
          Stage, 
          Submission, 
          Decision,
          Srn,
          Dcn,
        )
        .join(Adr.facility)
        .join(Adr.patient)
        .join(Adr.stages)
          .join(Stage.submissions)
            .join(Submission.auditor)
          .join(Stage.decisions)
        .join(Adr.srns)
          # .join(Srn.payments)
        .join(Adr.dcns)
        # .filter(Stage.stage=="180")
        .where(Adr.adr_id==10147)
        # .order_by(Adr.adr_id, Stage.stage.desc())

      )
      result = session.execute(stmt)
      # print(result.all())
      data = []
      for row in result.all():
        # print(row._mapping[Adr].as_dict())
        # print(row._mapping[Facility].as_dict())
        # print(row._mapping[Stage].as_dict())
        # print(row)
        data.append({
          'adr': row._mapping[Adr].as_dict(),
          'facility': row._mapping[Facility].as_dict(),
          'stage': row._mapping[Stage].as_dict(),
          'srn': row._mapping[Srn].as_dict(),
        })

      
      return {'data': data }
   
def dashboard_query(args):
  with Session(engine) as session:
    adrs_stmt = (
      select(Adr, Facility, Patient)
      .join(Adr.facility)
      .join(Adr.patient)
    )
    # stages_stmt = (
    #   select(Stage)
    #   .join(Stage.adr)
    # )
    # submissions_stmt = (
    #   select(Submission, Stage.adr_id)
    #   .join(Submission.stage)
    # )
    # decisions_stmt = (
    #   select(Decision, Stage.adr_id)
    #   .join(Decision.stage)
    # )

    adrs_result = session.execute(adrs_stmt)
    # stages_result = session.execute(stages_stmt)
    # submissions_result = session.execute(submissions_stmt)
    # decisions_result = session.execute(decisions_stmt)
    
    def row_unpack(row):
      return {k:v for tuple in row.tuple() for k, v in tuple.as_dict().items()}
    
    data = []
    for row in adrs_result.all():
      row_dict = row_unpack(row)

      data.append(row_dict)

    # df = pd.DataFrame(data)
    # print(df.head())

    return { 'data': data }

  return 



## Routes
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

@app.get("/full_query")
async def full_route():
  data = full_query('Adr')
  return data

@app.get("/dashboard")
async def dash_route():
  data = dashboard_query('Adr')
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
