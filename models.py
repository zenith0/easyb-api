from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Expense(Base):
    __tablename__ = 'expenses'
    id = Column(String, primary_key=True)
    reference = Column(String)
    amount = Column(String)
    matcher = Column(String)

class Income(Base):
    __tablename__ = 'income'
    id = Column(String, primary_key=True)
    reference = Column(String)
    amount = Column(String)
    matcher = Column(String)

class Accounting(Base):
    __tablename__ = 'accounting'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4())[:8])
    date = Column(String)
    transaction_date = Column(String)
    amount = Column(String)
    reference = Column(String)

engine = create_engine('sqlite:///data.db')
Base.metadata.create_all(engine)
