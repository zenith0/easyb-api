from sqlalchemy import create_engine, Column, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
import uuid

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(String, primary_key=True)
    reference = Column(String)
    amount = Column(Numeric(precision=10, scale=2))
    matcher = Column(String)

class Income(Base):
    __tablename__ = 'income'
    id = Column(String, primary_key=True)
    reference = Column(String)
    amount = Column(Numeric(precision=10, scale=2))
    matcher = Column(String)

class Accounting(Base):
    __tablename__ = 'accounting'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4())[:8])
    date = Column(Date)
    transaction_date = Column(Date)
    amount = Column(Numeric(precision=10, scale=2))
    reference = Column(String)

engine = create_engine('postgresql+psycopg2://postgres:easybankrulez@postgres:5432/easybank')
Base.metadata.create_all(engine)
