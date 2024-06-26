from fastapi import FastAPI
import sqlite3
import json

app = FastAPI()

def get_data(tablename, limit):
  # Connect to DB and create a cursor
  DATABASE_URL = "radr.db"
  sqliteConnection = sqlite3.connect(DATABASE_URL)
  cursor = sqliteConnection.cursor()
  print('DB Init')

  querystr = (f'SELECT * FROM {tablename} LIMIT {limit}')
  res = cursor.execute(querystr).fetchall()

  cursor.close()
  sqliteConnection.close()
  
  keys = list(map(lambda x: x[0], cursor.description))
  
  data = {'data': [
    {keys[i]: r[i] for i in range(0, len(keys))} for r in res
  ]}

  return data


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/facilities")
async def get_facilities():
  data = get_data('facilities', 5)
  return data


@app.get("/patients")
async def get_patients():
    data = get_data('patients', 5)
    return data

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
