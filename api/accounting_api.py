from flask import jsonify, request
from sqlalchemy.orm import sessionmaker
from models import Accounting, engine
from datetime import datetime

Session = sessionmaker(bind=engine)
session = Session()

class AccountingAPI:
    @staticmethod
    def get_accounting():
        accounting = session.query(Accounting).all()
        return jsonify([{
            'id': entry.id,
            'date': entry.date,
            'transaction_date': entry.transaction_date,
            'amount': entry.amount,
            'reference': entry.reference
        } for entry in accounting])

    @staticmethod
    def add_accounting():
        data = request.json
        if not all(key in data for key in ['date', 'transaction_date', 'amount', 'reference']):
            return jsonify({'error': 'Missing required fields'}), 400

        try:
            new_entry = Accounting(**data)
            session.add(new_entry)
            session.commit()
            return jsonify({'message': 'Entry added successfully', 'id': new_entry.id}), 201
        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 500
        

    @staticmethod
    def get_accounting_by_timeframe(start_date, end_date):
        try:
            start_date = datetime.strptime(start_date, '%d.%m.%Y')
            end_date = datetime.strptime(end_date, '%d.%m.%Y')
        except ValueError:
            return jsonify({'error': 'Invalid date format. Please use DD.MM.YYYY'}), 400

        accounting = session.query(Accounting).filter(
            Accounting.accounting_date.between(start_date, end_date)
        ).all()

        return jsonify([{
            'id': entry.id,
            'date': entry.date,
            'transaction_date': entry.transaction_date,
            'amount': entry.amount,
            'reference': entry.reference
        } for entry in accounting])

    # only available in debug mode    
    @staticmethod
    def delete_all_accounting(enabled=False):
        if not enabled:
            return jsonify({'error': 'This endpoint is only available in debug mode'}), 403

        try:
            session.query(Accounting).delete()
            session.commit()
            return jsonify({'message': 'All accounting data deleted successfully'}), 200
        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 500