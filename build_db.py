
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import insert
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session
import generator
from Classes import *
# from Classes import Patient
# from Classes import Auditor
# from Classes import Adr
# from Classes import Stage
# from Classes import Submission
# from Classes import Decision
# from Classes import Srn
# from Classes import Dcn

tables = {
			'facility'   	: Facility,
			'patient'     : Patient,
			'auditor'     : Auditor,
			'adr'         : Adr,
			'stage'       : Stage,
			'submission'  : Submission,
			'decision'    : Decision,
			'srn'         : Srn,
			'dcn'         : Dcn,
	}

def main():
	# CONNECTION
	print("CONNECTING DATABASE")
	engine = create_engine("sqlite+pysqlite:///radr.db", echo=True)

	# Build Tables
	print("BUILDING TABLES")
	Base.metadata.create_all(engine)

	# Generate Random Data
	print("GENERATING DATA")
	data = generator.generate_data(export=False)


	# Insert into Tables

	with Session(engine) as session:
		for table_name in tables.keys():
			print(f"Inserting into {table_name} table")
			session.execute(
				insert(tables[table_name]),
				data[table_name],
			)
			

if __name__ == "__main__":
	main()