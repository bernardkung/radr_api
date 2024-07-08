# from sqlalchemy import MetaData, Table, Column, Integer, Float, String, Date, Boolean, ForeignKey, create_engine, insert
from sqlalchemy import create_engine, DateTime
import generator
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

import datetime

# CONNECTION
engine = create_engine("sqlite+pysqlite:///radr.db", echo=True)


# DEFINING TABLES
class Base(DeclarativeBase):
	pass

class Facility(Base):
	__tablename__ = "facility"

	global_id: Mapped[int] = mapped_column(primary_key=True)
	dl_id: Mapped[int]
	dl_name: Mapped[str]
	mac: Mapped[str]
	npi: Mapped[int]
	revenue_center: Mapped[str]
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

	def __repr__(self) -> str:
			return f"Facility(global_id={self.global_id!r}, dl_id={self.dl_id!r}, dl_name={self.dl_name!r}), mac={self.mac!r}), npi={self.npi!r}), revenue_center={self.revenue_center!r})"


class Auditor(Base):
	__tablename__ = "auditor"

	auditor_id: Mapped[int] = mapped_column(primary_key=True)
	auditor_name: Mapped[str]
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())


class Patient(Base):
	__tablename__ = "patient"

	mrn: Mapped[int] = mapped_column(primary_key=True)
	first_name: Mapped[str]
	last_name: Mapped[str]
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())


class Adr(Base):
	__tablename__ = "adr"

	adr_id: Mapped[int] = mapped_column(primary_key=True)
	global_id: Mapped[Facility] = relationship()
	mrn: Mapped[Patient] = relationship()
	from_date: Mapped[datetime.date]
	to_date: Mapped[datetime.date]
	expected_reimbursement: Mapped[float]
	active: Mapped[bool]
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	

class Stage(Base):
	__tablename__ = "table"

	stage_id: Mapped[int] = mapped_column(primary_key=True)
	adr_id: Mapped[Adr] = relationship()
	stage: Mapped[str]
	notification_date: Mapped[datetime.date]
	due_date: Mapped[datetime.date]
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	

class Submission(Base):
	__tablename__ = "submission"

	submission_id: Mapped[int] = mapped_column(primary_key=True)
	stage_id: Mapped[Stage] = relationship()
	auditor_id: Mapped[Auditor] = relationship()
	submission_date: Mapped[datetime.date]
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	

class Decision(Base):
	__tablename__ = "decision"

	decision_id: Mapped[int] = mapped_column(primary_key=True)
	stage_id: Mapped[Stage] = relationship()
	decision_date: Mapped[datetime.date]
	decision: Mapped[str]
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	

class Srn(Base):
	__tablename__ = "srn"

	srn: Mapped[str] = mapped_column(primary_key=True)
	adr_id: Mapped[Stage] = relationship()
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	

class Dcn(Base):
	__tablename__ = "dcn"

	dcn: Mapped[str] = mapped_column(primary_key=True)
	adr_id: Mapped[Stage] = relationship()
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	



# Build Tables
Base.metadata.create_all(engine)


# Generate Random Data
data = generator.generate_data(export=False)

# Insert into Tables
for dk, dv in data.items():
	print(dk)