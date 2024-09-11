from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import sqlite3
import json
import pandas as pd
from sqlalchemy import create_engine, text, select, func, desc
from sqlalchemy.orm import Session, aliased, join, joinedload
from Classes import *
from sqlalchemy.sql import exists
app = FastAPI()


## Engine configuration
origins = [
  "*"
]

# Middleware
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

# Mount Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

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


def get_column(table, column_name):
  # Ensure the column exists in the model
  if column_name not in table.__table__.columns:
    raise IndexError
  else:
    column_attr = getattr(table, column_name)
    return column_attr


def query(args):
  with Session(engine) as session:
    table = tables[ args['table_name'] ]
    
    ## Build query
    stmt = select(table)  
    # if ( args['full'] == False ):
    #   stmt = select(table)  

    # ## Join
    # elif ( args['full'] == True ):
    #   stmt = (select(Adr, func.max())
    #     .join(Adr.stages)
    #       .join(Stage.submissions)
    #         .join(Submission.auditor)
    #       .join(Stage.decisions)
    #     .join(Adr.srns)
    #       .join(Srn.payments)
    #     .join(Adr.dcns)
    #   )
      
    
    ## Filter
    if (args['filter_column'] is not None) and (args['filter_value'] is not None):
      column_attr = get_column(table, args['filter_column'])
      stmt = stmt.filter( column_attr == args['filter_value'] )

    ## Execute Query
    result = session.execute(stmt)

    data = []
    for row in result.all():
      data.append(row._mapping[ table ].as_dict())
    
    return {'data': data }
  
def query_adrs(args):
  with Session(engine) as session:
    table = tables[ args['table_name'] ]
    
    ## Build query
    if ( args['full'] == False ):
      stmt = select(Adr)  

    ## Join
    elif ( args['full'] == True ):
      stmt = (
        select(Facility, Patient, Adr)
        .join(Adr.facility)
        .join(Adr.patient)
        .options(
          joinedload(Adr.stages)
          .options(
            joinedload(Stage.submissions).joinedload(Submission.auditor),
            joinedload(Stage.decisions)
          ),
          joinedload(Adr.srns)
          .options(
            joinedload(Srn.payments)
          )
        )
      )
      
    
    ## Filter
    if (args['filter_column'] is not None) and (args['filter_value'] is not None):
      column_attr = get_column(table, args['filter_column'])
      stmt = stmt.filter( column_attr == args['filter_value'] )

    ## Execute Query
    result = session.execute(stmt).unique()

    data = []
    for row in result.all():
      data.append(row._mapping)
    
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

def dev_query(args):
  with Session(engine) as session:
    ## Defining Statements
    kpm_stmts = {
      'adr_count': (
        select(func.count(Adr.adr_id))
      ),
      'expreimb_sum': (
        select(func.sum(Adr.expected_reimbursement))
      ),
      'payment_sum': (
        select(func.sum(Payment.payment_amount))
      ),
      # 'due_count': (
      #   select(func.count(Stage.stage_id)))
      #   .filter((~exists().where(Stage.stage_id == Submission.stage_id))
      # )
    }

    # session.query(Ticker).order_by(desc('updated')).first()

    ## Executing Statments
    results = { key:session.execute(stmt) for key, stmt in kpm_stmts.items() }
    
    ## Unpacking Results
    data = {}
    for key, result in results.items():
      data[key] = round(result.scalars().one(), 2)


    return { 'data': data }
  
def query_stages(args):
  with Session(engine) as session:
    ## Defining Statements
    stmt = (session.query(
        Stage, 
        func.sum(Payment.payment_amount).label('net_payment'),
        func.avg(Adr.expected_reimbursement).label('expected_reimbursement'),
      )
      .join(Adr.stages)
      .join(Adr.srns)
      .join(Srn.payments)
      .group_by(Stage)
    )

    if args['stage_id'] is not None:
      stmt = stmt.filter(Stage.stage_id==args['stage_id'])
    if args['submitted']==True:
      stmt = stmt.filter(exists().where(Stage.stage_id == Submission.stage_id))
    if args['submitted']==False:
      stmt = stmt.filter(~exists().where(Stage.stage_id == Submission.stage_id))

    ## Executing Statments
    result = session.execute(stmt)
    
    testrow = result.fetchone()
    ## Unpacking Results
    data = {}
    data['stages'] = [ row._mapping for row in result.all()]
    # data['stages'] = [ {
    #   **testrow.Stage.as_dict(), 
    #   'net_payment': testrow.net_payment,
    #   'expected_reimbursement': row.expected_reimbursement,
    # } for row in result.all() ]
      

    return { 'data': data }


def dashboard_query(args):
  with Session(engine) as session:
    adrs_stmt = (
      select(Adr, Facility, Patient)
      .join(Adr.facility)
      .join(Adr.patient)
    )


    stages_stmt = (
      select(Stage)
      .join(Stage.adr)
    )
    submissions_stmt = (
      select(Submission, Stage.adr_id)
      .join(Submission.stage)
    )
    decisions_stmt = (
      select(Decision, Stage.adr_id)
      .join(Decision.stage)
    )
    payments_stmt = (
      select(Payment, Srn.adr_id)
      .join(Payment.srn)
    )

    stmts = {
      "adrs": adrs_stmt, 
      "stages": stages_stmt, 
      "submissions": submissions_stmt, 
      "decisions": decisions_stmt,
      "payments": payments_stmt,
    }

    results = { key:session.execute(stmt) for key, stmt in stmts.items() }

    def row_unpack(row):
      return {k:v for tuple in row.tuple() for k, v in tuple.as_dict().items()}
      
    def processor(key, result):
      data = []
      for row in result.all():
        if key in ['adrs']:
          row_dict = row_unpack(row)
        elif key in ['decisions', 'submissions', 'payments']:
          row_dict = {'adr_id': row[1], **row[0].as_dict()}
        elif key in ['stages']:
          row_dict = row._asdict()['Stage']
        else:
          print(row)
        data.append( row_dict ) 
      return data
  
    data = {}
    for key, result in results.items():
      data[key]=processor(key, result)

    return { 'data': data }

  return 



## Routes
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
  favicon_path = './static/favicon.ico'
  return FileResponse(favicon_path)

@app.get("/facilities")
async def get_facilities(filter_column: str = 'global_id', global_id: int = None):
  data = query({
    'table_name': 'Facility',
    'filter_column': filter_column,
    'filter_value': global_id,
  })
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
async def get_adrs(full: bool = False, filter_column: str = 'adr_id', adr_id: int = None):
  data = query_adrs({
    'table_name': 'Adr', 
    'filter_column': filter_column,
    'filter_value': adr_id,
    'full': full,
  })
  return data

@app.get("/full_query")
async def full_route():
  data = full_query('Adr')
  return data

@app.get("/dashboard")
async def dash_route():
  data = dashboard_query('Adr')
  return data

@app.get("/dev")
async def dev_route():
  data = dev_query('Adr')
  return data

@app.get("/stages")
async def get_stages(stage_id: int = None, submitted: bool = None):
  data = query_stages(args={'stage_id': stage_id, 'submitted': submitted})
  return data

@app.get("/submissions")
async def get_submissions(filter_column: str = 'submission_id', submission_id: int = None):  
  data = query({
    'table_name': 'Submission',
    'filter_column': filter_column,
    'filter_value': submission_id,
  })
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
