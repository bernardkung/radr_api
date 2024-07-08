from sqlalchemy import MetaData, Table, Column, Integer, Float, String, Date, Boolean, ForeignKey, create_engine, insert

# CONNECTION
engine = create_engine("sqlite+pysqlite:///radr.db", echo=True)


# DEFINING TABLES
metadata_obj = MetaData()

facilities_tables = Table(
    "facilities",
    metadata_obj,
    Column("global_id", Integer, primary_key=True),
    Column("dl_id", Integer),
    Column("dl_name", String),
    Column("mac", String),
    Column("npi", Integer),
    Column("revenue_center", String),
)

auditors_table = Table(
    "auditors",
    metadata_obj,
    Column("auditor_id", Integer, primary_key=True),
    Column("auditor_name", String),
)

patients_table = Table(
    "patients",
    metadata_obj,
    Column("mrn", Integer, primary_key=True),
    Column("first_name", String),
    Column("last_name", String),
)

adrs_table = Table(
    "adrs",
    metadata_obj,
    Column("adr_id", Integer, primary_key=True),
    Column("global_id", ForeignKey("facilities.global_id"), nullable=False),
    Column("mrn", ForeignKey("patients.mrn"), nullable=False),
    Column("from_date", Date),
    Column("to_date", Date),
    Column("expected_reimbursement", Float),
    Column("active", Boolean, nullable=False),
)

stages_table = Table(
    "stages",
    metadata_obj,
    Column("stage_id", Integer, primary_key=True),
    Column("adr_id", ForeignKey("adrs.adr_id"), nullable=False),
    Column("stage", String, nullable=False),
    Column("notification_date", Date),
    Column("due_date", Date),
)

submissions_table = Table(
    "submissions",
    metadata_obj,
    Column("submission_id", Integer, primary_key=True),
    Column("stage_id", ForeignKey("stages.stage_id"), nullable=False),
    Column("auditor_id", ForeignKey("auditors.auditor_id"), nullable=False),
    Column("submission_date", Date, nullable=False),
)

decisions_table = Table(
    "decisions",
    metadata_obj,
    Column("decision_id", Integer, primary_key=True),
    Column("stage_id", ForeignKey("stages.stage_id"), nullable=False),
    Column("decision_date", Date, nullable=False),
    Column("decision", Date, nullable=False),
)

srns_table = Table(
    "srns",
    metadata_obj,
    Column("srn", String, primary_key=True),
    Column("adr_id", ForeignKey("adrs.adr_id"), nullable=False),
)

dcns_table = Table(
    "dcns",
    metadata_obj,
    Column("dcn", String, primary_key=True),
    Column("adr_id", ForeignKey("adrs.adr_id"), nullable=False),
)


# Build Tables
metadata_obj.create_all(engine)