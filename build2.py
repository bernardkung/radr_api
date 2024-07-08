from sqlalchemy import MetaData, Table, Column, Integer, Float, String, Date, Boolean, ForeignKey


metadata_obj = MetaData()

facilities_tables = Table(
    "facilities",
    metadata_obj,
    Column("global_id", Integer(6), primary_key=True),
    Column("dl_id", Integer(4)),
    Column("dl_name", String),
    Column("mac", String),
    Column("npi", Integer(10)),
    Column("revenue_center", String),
)

auditors_table = Table(
    "auditors",
    metadata_obj,
    Column("auditor_id", Integer(7), primary_key=True),
    Column("auditor_name", String),
)

patients_table = Table(
    "patients",
    metadata_obj,
    Column("mrn", Integer(9), primary_key=True),
    Column("first_name", String),
    Column("last_name", String),
)

adrs_table = Table(
    "adr",
    metadata_obj,
    Column("adr_id", Integer, primary_key=True),
    Column("global_id", ForeignKey("facilities.global_id"), nullable=False),
    Column("mrn", ForeignKey("patients.mrn"), nullable=False),
    Column("from_date", Date),
    Column("from_date", Date),
    Column("expected_reimbursement", float),
    Column("active", Boolean, nullable=False),
)



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
	