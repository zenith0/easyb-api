from flask import jsonify, request
from sqlalchemy.orm import sessionmaker
from models import Expense, engine

Session = sessionmaker(bind=engine)
session = Session()

class ExpenseAPI:
    @staticmethod
    def get_expenses():
        expenses = session.query(Expense).all()
        return jsonify([{
            'id': expense.id,
            'reference': expense.reference,
            'amount': expense.amount,
            'matcher': expense.matcher
        } for expense in expenses])

    @staticmethod
    def add_expense():
        data = request.json
        new_expense = Expense(**data)
        session.add(new_expense)
        session.commit()
        return jsonify({'message': 'Expense added successfully', 'id': new_expense.id}), 201

    @staticmethod
    def update_expense(expense_id):
        expense = session.query(Expense).filter_by(id=expense_id).first()
        if expense:
            data = request.json
            for key, value in data.items():
                setattr(expense, key, value)
            session.commit()
            return jsonify({'message': 'Expense updated successfully'}), 200
        else:
            return jsonify({'message': 'Expense not found'}), 404

    @staticmethod
    def delete_expense(expense_id):
        expense = session.query(Expense).filter_by(id=expense_id).first()
        if expense:
            session.delete(expense)
            session.commit()
            return jsonify({'message': 'Expense deleted successfully'}), 200
        else:
            return jsonify({'message': 'Expense not found'}), 404
