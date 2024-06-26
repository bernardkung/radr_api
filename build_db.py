import sqlite3
import generator
import json


def drop_table(table_name, cursor, debug=True):
	# DROP TABLE
	print(f"Resetting {table_name.upper()} table")
	dropquery = f"DROP TABLE IF EXISTS {table_name};"
	if debug:
		print(dropquery)
	cursor.execute(dropquery)

def create_table(table_name, columns, relationships, cursor, debug=True):
	# CREATE TABLE
	print(f"Building {table_name.upper()} table")
	# use column dict to build query string
	colstring = ""
	for col in columns:
		colstring += f"{col['name']} {col['type']} ({col['len'] if len in col.keys() else 255}) {col['clauses'] if 'clauses' in col.keys() else ''},"
	
	relstring = ""
	for rel in relationships:
		relstring += f", FOREIGN KEY({rel['fk']}) REFERENCES {rel['table']}({rel['pk']})"
	
	buildquery = f"CREATE TABLE {table_name} ({colstring[0:-1]} {relstring})"

	print(buildquery)
	if debug:
		print(buildquery)
	cursor.execute(buildquery)

def insert_table(table_name, columns, data, cursor, debug):
	# INSERT DATA INTO TABLE
	print(f"Populating {table_name.upper()} table")
	key_list = [column['name'].lower() for column in columns]
	key_str = ",".join(key_list)
	val_list = [":" + key for key in key_list]
	val_str = ",".join(val_list)
	insertquery = (f"INSERT INTO {table_name} "
					f"({key_str})" 
					"VALUES "
					f"({val_str})")
	if debug:
		print(insertquery)
	cursor.executemany(insertquery, data[table_name])

def build_table(table_name, columns, relations, data, cursor, debug=True):

	drop_table(table_name, cursor, debug)
	create_table(table_name, columns, relations, cursor, debug)
	insert_table(table_name, columns, data, cursor, debug)



try:

	# Connect to DB and create a cursor
	sqliteConnection = sqlite3.connect('radr.db')
	cursor = sqliteConnection.cursor()
	print('DB Init')

	# Generate Random Data
	data = generator.generate_data(export=False)

	## FACILTIIES
	facilities_columns = [
		{'name': 'GLOBAL_ID', 			'type': 'INTEGER', 'len': 6, 'clauses': 'PRIMARY KEY'},
		{'name': 'DL_ID', 					'type': 'INTEGER', 'len': 4},
		{'name': 'DL_NAME', 				'type': 'TEXT'},
		{'name': 'MAC', 						'type': 'TEXT'},
		{'name': 'NPI', 						'type': 'INTEGER', 'len': 10},
		{'name': 'REVENUE_CENTER', 	'type': 'TEXT', },
	]
	facilities_relationships = []
	build_table('facilities', facilities_columns, facilities_relationships, data, cursor, debug=False)

	## AUDITORS
	auditors_columns = [
		{'name': 'AUDITOR_ID', 			'type': 'INTEGER', 'len': 7, 'clauses': 'PRIMARY KEY'},
		{'name': 'AUDITOR_NAME',		'type': 'TEXT'},
	]
	auditors_relationships = []
	build_table('auditors', auditors_columns, auditors_relationships, data, cursor, debug=False)

	patients_columns = [
		{'name': 'MRN',					'type': 'INTEGER', 'len': 9, 'clauses': 'PRIMARY KEY'},
		{'name': 'FIRST_NAME',	'type': 'TEXT'},
		{'name': 'LAST_NAME',		'type': 'TEXT'},
	]
	patients_relationships = []
	build_table('patients', patients_columns, patients_relationships, data, cursor, debug=False)

	## ADRS
	adrs_columns = [
		{'name': 'ADR_ID', 									'type': 'INTEGER', 'clauses': 'PRIMARY KEY'},
		{'name': 'GLOBAL_ID', 							'type': 'TEXT', 'clauses': 'NOT NULL'},
		{'name': 'MRN', 										'type': 'TEXT', 'clauses': 'NOT NULL'},
		# {'name': 'NOTIFICATION_DATE',				'type': 'INTEGER', 'len': 4},
		{'name': 'FROM_DATE',								'type': 'TEXT'},
		{'name': 'TO_DATE',									'type': 'TEXT'},
		{'name': 'EXPECTED_REIMBURSEMENT',	'type': 'REAL', 'len': 8},
		{'name': 'ACTIVE', 									'type': 'INTEGER',  'clauses': 'NOT NULL'}, # 0==False,1==True
	]
	adrs_relationships = [
		{'fk': 'GLOBAL_ID', 'table': 'FACILITIES', 'pk': 'GLOBAL_ID'},
		{'fk': 'MRN', 'table': 'PATIENTS', 'pk': 'MRN'},
	]
	build_table('adrs', adrs_columns, adrs_relationships, data, cursor, debug=False)

	## STAGES
	stages_columns = [
		{'name': 'STAGE_ID', 								'type': 'INTEGER', 'clauses': 'PRIMARY KEY'},
		{'name': 'ADR_ID', 									'type': 'INTEGER', 'clauses': 'NOT NULL'},
		{'name': 'STAGE', 									'type': 'TEXT', 'clauses': 'NOT NULL'},
		{'name': 'NOTIFICATION_DATE',				'type': 'TEXT', 'clauses': 'NOT NULL'},
		{'name': 'DUE_DATE',								'type': 'TEXT', 'clauses': 'NOT NULL'},
	]
	stages_relationships = [
		{'fk': 'ADR_ID', 'table': 'ADRS', 'pk': 'ADR_ID'},
	]
	build_table('stages', stages_columns, stages_relationships, data, cursor, debug=False)

	## SUBMISSIONS
	submissions_columns = [
		{'name': 'SUBMISSION_ID',		'type': 'INTEGER', 'clauses': 'PRIMARY KEY'},
		{'name': 'STAGE_ID',				'type': 'INTEGER', 'clauses': 'NOT NULL'},
		{'name': 'SUBMISSION_DATE',	'type': 'TEXT', 'clauses': 'NOT NULL'},
		{'name': 'AUDITOR_ID',			'type': 'INTEGER', 'clauses': 'NOT NULL'},
	]
	submissions_relationships = [
		{'fk': 'STAGE_ID', 'table': 'STAGES', 'pk': 'STAGE_ID'},
	]
	build_table('submissions', submissions_columns, submissions_relationships, data, cursor, debug=False)

	## DECISIONS
	decisions_columns = [
		{'name': 'DECISION_ID',		'type': 'INTEGER', 'clauses': 'PRIMARY KEY'},
		{'name': 'STAGE_ID',			'type': 'INTEGER', 'clauses': 'NOT NULL'},
		{'name': 'DECISION_DATE',	'type': 'TEXT', 'clauses': 'NOT NULL'},
		{'name': 'DECISION',			'type': 'TEXT', 'clauses': 'NOT NULL'},
	]
	decisions_relationships = [
		{'fk': 'STAGE_ID', 'table': 'STAGES', 'pk': 'STAGE_ID'},
	]
	build_table('decisions', decisions_columns, decisions_relationships, data, cursor, debug=False)

	## SRNS
	srns_columns = [
		{'name': 'SRN',			'type': 'TEXT', 'len': 12, 'clauses': 'PRIMARY KEY'},
		{'name': 'ADR_ID',	'type': 'INTEGER', 'clauses': 'NOT NULL'},
	]
	srns_relationships = [
		{'fk': 'ADR_ID', 'table': 'ADRS', 'pk': 'ADR_ID'},
	]
	build_table('srns', srns_columns, srns_relationships, data, cursor, debug=False)
	
	## DCNS
	dcns_columns = [
		{'name': 'DCN',			'type': 'TEXT', 'len': 17, 'clauses': 'PRIMARY KEY'},
		{'name': 'ADR_ID',	'type': 'INTEGER', 'clauses': 'NOT NULL'},
	]
	dcns_relationships = [
		{'fk': 'ADR_ID', 'table': 'ADRS', 'pk': 'ADR_ID'},
	]
	build_table('dcns', dcns_columns, dcns_relationships, data, cursor, debug=False)
	
	# SELECT FROM FACILITIES
	# selectfacilities = ("PRAGMA table_info(stages);")
	# ret = cursor.execute(selectfacilities)
	# print(ret)

	# Fetch and output result
	# result = cursor.fetchall()
	# jsonresult = json.dumps(result)
	# print(jsonresult)
	# print('{}'.format(jsonresult))

	# Close the cursor
	cursor.close()
	sqliteConnection.commit()



# Handle errors
except sqlite3.Error as error:
	print('Error occurred - ', error)



# Close DB Connection irrespective of success
# or failure
finally:

	if sqliteConnection:
		sqliteConnection.close()
		print('SQLite Connection closed')
