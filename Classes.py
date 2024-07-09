# from sqlalchemy import MetaData, Table, Column, Integer, Float, String, Date, Boolean, ForeignKey, create_engine, insert
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
# from sqlalchemy import String
# from sqlalchemy import insert
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime



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
	adrs: Mapped[List["Adr"]] = relationship(back_populates="facility")

	def __repr__(self) -> str:
			return f"Facility(global_id={self.global_id!r}, dl_id={self.dl_id!r}, dl_name={self.dl_name!r}), mac={self.mac!r}), npi={self.npi!r}), revenue_center={self.revenue_center!r})"


class Auditor(Base):
	__tablename__ = "auditor"

	auditor_id: Mapped[int] = mapped_column(primary_key=True)
	auditor_name: Mapped[str]
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	submissions: Mapped[List["Submission"]] = relationship(back_populates="auditor")


class Patient(Base):
	__tablename__ = "patient"

	mrn: Mapped[int] = mapped_column(primary_key=True)
	first_name: Mapped[str]
	last_name: Mapped[str]
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	adrs: Mapped[List["Adr"]] = relationship(back_populates="patient")


class Adr(Base):
	__tablename__ = "adr"

	adr_id: Mapped[int] = mapped_column(primary_key=True)

	global_id = mapped_column(ForeignKey("facility.global_id"))
	facility: Mapped[Facility] = relationship(back_populates="adrs")  

	mrn = mapped_column(ForeignKey("patient.mrn"))
	patient: Mapped[Patient] = relationship(back_populates="adrs")

	from_date: Mapped[datetime.date]
	to_date: Mapped[datetime.date]
	expected_reimbursement: Mapped[float]
	active: Mapped[bool]
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	stages: Mapped[List["Stage"]] = relationship(back_populates="adr")
	srns: Mapped[List["Srn"]] = relationship(back_populates="adr")
	dcns: Mapped[List["Dcn"]] = relationship(back_populates="adr")
	

class Stage(Base):
	__tablename__ = "stage"

	stage_id: Mapped[int] = mapped_column(primary_key=True)
	adr_id = mapped_column(ForeignKey("adr.adr_id"))
	adr: Mapped[Adr] = relationship(back_populates="stages")
	stage: Mapped[str]
	notification_date: Mapped[datetime.date]
	due_date: Mapped[datetime.date]
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	submissions: Mapped[List["Submission"]] = relationship(back_populates="stage")
	decisions: Mapped[List["Decision"]] = relationship(back_populates="stage")
	

class Submission(Base):
	__tablename__ = "submission"

	submission_id: Mapped[int] = mapped_column(primary_key=True)

	stage_id = mapped_column(ForeignKey("stage.stage_id"))
	stage: Mapped[Stage] = relationship(back_populates="submissions")

	auditor_id = mapped_column(ForeignKey("auditor.auditor_id"))
	auditor: Mapped[Auditor] = relationship(back_populates="submissions")

	submission_date: Mapped[datetime.date]
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	

class Decision(Base):
	__tablename__ = "decision"

	decision_id: Mapped[int] = mapped_column(primary_key=True)
	stage_id = mapped_column(ForeignKey("stage.stage_id"))
	stage: Mapped[Stage] = relationship(back_populates="decisions")
	decision_date: Mapped[datetime.date]
	decision: Mapped[str]
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	

class Srn(Base):
	__tablename__ = "srn"

	srn: Mapped[str] = mapped_column(primary_key=True)
	adr_id = mapped_column(ForeignKey("adr.adr_id"))
	adr: Mapped[Adr] = relationship(back_populates="srns")
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	

class Dcn(Base):
	__tablename__ = "dcn"

	dcn: Mapped[str] = mapped_column(primary_key=True)
	adr_id = mapped_column(ForeignKey("adr.adr_id"))
	adr: Mapped[Adr] = relationship(back_populates="dcns")
	created_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	updated_date: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
	

def main():
	# CONNECTION
	print("CONNECTING DATABASE")
	engine = create_engine("sqlite+pysqlite:///radr.db", echo=True)

	# Build Tables
	print("BUILDING TABLES")
	Base.metadata.create_all(engine)

if __name__ == "__main__":
	main()