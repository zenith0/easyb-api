from flask import jsonify, request
from sqlalchemy.orm import sessionmaker
from models import Income, engine

Session = sessionmaker(bind=engine)
session = Session()

class IncomeAPI:
    @staticmethod
    def get_income():
        income = session.query(Income).all()
        return jsonify([{
            'id': income_item.id,
            'reference': income_item.reference,
            'amount': income_item.amount,
            'matcher': income_item.matcher
        } for income_item in income])

    @staticmethod
    def add_income():
        data = request.json
        new_income = Income(**data)
        session.add(new_income)
        session.commit()
        return jsonify({'message': 'Income added successfully', 'id': new_income.id}), 201

    @staticmethod
    def update_income(income_id):
        income_item = session.query(Income).filter_by(id=income_id).first()
        if income_item:
            data = request.json
            for key, value in data.items():
                setattr(income_item, key, value)
            session.commit()
            return jsonify({'message': 'Income updated successfully'}), 200
        else:
            return jsonify({'message': 'Income not found'}), 404

    @staticmethod
    def delete_income(income_id):
        income = session.query(Income).filter_by(id=income_id).first()
        if income:
            session.delete(income)
            session.commit()
            return jsonify({'message': 'Income deleted successfully'}), 200
        else:
            return jsonify({'message': 'Income not found'}), 404
