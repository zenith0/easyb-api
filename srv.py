from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json
import uuid

# Initialize Flask app
app = Flask(__name__)

# Configure PostgreSQL connection
POSTGRES_USER = 'postgres'
POSTGRES_PW = 'easybankrulez'
POSTGRES_DB = 'easybank'
POSTGRES_HOST = 'postgres'
POSTGRES_PORT = '5432'

# Define the connection string
connection_str = f'postgresql://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

# Create the SQLAlchemy engine
engine = create_engine(connection_str)

# Create the session
Session = sessionmaker(bind=engine)
session = Session()

# Define the base model
Base = declarative_base()

# Define the database models
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

# Create the tables
Base.metadata.create_all(engine)

# Routes for CRUD operations
@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = session.query(Expense).all()
    return jsonify([{
        'id': expense.id,
        'reference': expense.reference,
        'amount': expense.amount,
        'matcher': expense.matcher
    } for expense in expenses])

@app.route('/expenses', methods=['POST'])
def add_expense():
    data = request.json
    if 'id' not in data:
        data['id'] = str(uuid.uuid4())[:8]  # Generate a random ID if not provided
    new_expense = Expense(
        id=data['id'],
        reference=data['reference'],
        amount=data['amount'],
        matcher=data['matcher']
    )
    session.add(new_expense)
    session.commit()
    return jsonify({'message': 'Expense added successfully', 'id': new_expense.id}), 201

@app.route('/expenses/<expense_id>', methods=['PUT'])
def update_expense(expense_id):
    expense = session.query(Expense).filter_by(id=expense_id).first()
    if expense:
        data = request.json
        expense.reference = data.get('reference', expense.reference)
        expense.amount = data.get('amount', expense.amount)
        expense.matcher = data.get('matcher', expense.matcher)
        session.commit()
        return jsonify({'message': 'Expense updated successfully'}), 200
    else:
        return jsonify({'message': 'Expense not found'}), 404

@app.route('/expenses/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expense = session.query(Expense).filter_by(id=expense_id).first()
    if expense:
        session.delete(expense)
        session.commit()
        return jsonify({'message': 'Expense deleted successfully'}), 200
    else:
        return jsonify({'message': 'Expense not found'}), 404

@app.route('/income', methods=['GET'])
def get_income():
    income = session.query(Income).all()
    return jsonify([{
        'id': income_item.id,
        'reference': income_item.reference,
        'amount': income_item.amount,
        'matcher': income_item.matcher
    } for income_item in income])

@app.route('/income', methods=['POST'])
def add_income():
    data = request.json
    if 'id' not in data:
        data['id'] = str(uuid.uuid4())[:8]  # Generate a random ID if not provided
    new_income = Income(
        id=data['id'],
        reference=data['reference'],
        amount=data['amount'],
        matcher=data['matcher']
    )
    session.add(new_income)
    session.commit()
    return jsonify({'message': 'Income added successfully', 'id': new_income.id}), 201

@app.route('/income/<income_id>', methods=['PUT'])
def update_income(income_id):
    income_item = session.query(Income).filter_by(id=income_id).first()
    if income_item:
        data = request.json
        income_item.reference = data.get('reference', income_item.reference)
        income_item.amount = data.get('amount', income_item.amount)
        income_item.matcher = data.get('matcher', income_item.matcher)
        session.commit()
        return jsonify({'message': 'Income updated successfully'}), 200
    else:
        return jsonify({'message': 'Income not found'}), 404

@app.route('/income/<income_id>', methods=['DELETE'])
def delete_income(income_id):
    income = session.query(Income).filter_by(id=income_id).first()
    if income:
        session.delete(income)
        session.commit()
        return jsonify({'message': 'Income deleted successfully'}), 200
    else:
        return jsonify({'message': 'Income not found'}), 404


# Similar routes for income items...

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
