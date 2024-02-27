from sqlalchemy import create_engine, Column, String, Date, Numeric, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Access environment variables
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PW = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_DB_PORT = os.getenv('POSTGRES_DB_PORT')

DATE_FORMAT = '%d-%m-%Y'


Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4())[:8])
    reference = Column(String)
    amount = Column(Numeric(precision=10, scale=2))
    matcher = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))

class Income(Base):
    __tablename__ = 'income'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4())[:8])
    reference = Column(String)
    amount = Column(Numeric(precision=10, scale=2))
    matcher = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))

class Accounting(Base):
    __tablename__ = 'accounting'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4())[:8])
    date = Column(Date)
    transaction_date = Column(Date)
    amount = Column(Numeric(precision=10, scale=2))
    reference = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))

class AccountingTotal(Base):
    __tablename__ = 'accounting_total'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4())[:8])
    date = Column(Date)
    total = Column(Numeric(precision=10, scale=2))

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    
db_url = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_HOST}:{POSTGRES_DB_PORT}/{POSTGRES_DB}"

engine = create_engine(db_url)
Base.metadata.create_all(engine)
