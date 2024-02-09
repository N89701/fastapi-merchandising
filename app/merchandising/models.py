import datetime

from sqlalchemy import (
    Boolean, Column, Integer, String, TIMESTAMP, Date, DateTime
)
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class Batch(Base):
    __tablename__ = "batch"

    id = Column(Integer, primary_key=True)
    status = Column(Boolean, default=False)
    assignment = Column(String, nullable=False)
    line = Column(String, nullable=False)
    shift = Column(String, nullable=False)
    squad = Column(String, nullable=False)
    number = Column(Integer, nullable=False, unique=True)
    date = Column(Date, nullable=False, unique=True)
    nomenclature = Column(String, nullable=False)
    codekn = Column(String, nullable=False, index=True)
    identificator_rc = Column(String, nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
    closed_at = Column(TIMESTAMP)


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False, unique=True, index=True)
    batch = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    is_aggregated = Column(Boolean, default=False)
    aggregated_at = Column(DateTime)
