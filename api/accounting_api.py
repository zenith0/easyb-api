from flask import jsonify, request
from sqlalchemy.orm import sessionmaker
from models import Accounting, AccountingTotal, engine, DATE_FORMAT
from sqlalchemy import desc
from datetime import datetime
import logging

Session = sessionmaker(bind=engine)
session = Session()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)  # Set logging level to DEBUG
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class AccountingAPI:
    # TODO: remove? Generally this shouldnt be used in reality
    @staticmethod
    def get_accounting():
        accounting = session.query(Accounting).all()
        return jsonify([{
            'id': entry.id,
            'date': entry.date.strftime(DATE_FORMAT),
            'transaction_date': entry.transaction_date.strftime(DATE_FORMAT),
            'amount': entry.amount,
            'reference': entry.reference
        } for entry in accounting])

    @staticmethod
    def _add_single_entry(data):
        if not all(key in data for key in ['date', 'transaction_date', 'amount', 'reference']):
            logger.error("Missing field for entry: %s", data)
            return jsonify({'error': 'Missing required fields'}), 400

        try:
        # Check if an entry with the same reference, date, and amount already exists
            date_str = data['date']
            date_obj = datetime.strptime(date_str, DATE_FORMAT)
            data['date']=date_obj
            date_str = data['transaction_date']
            date_obj = datetime.strptime(date_str, DATE_FORMAT)
            data['transaction_date']=date_obj
            existing_entry = session.query(Accounting).filter_by(
                reference=data['reference'],
                date=data['date'],
                amount=data['amount'],
                transaction_date=data['transaction_date']
            ).first()

            if existing_entry:
                logger.debug("Posted entry %s already exists: %s", data, existing_entry)                
                # Entry already exists, return its ID
                return {'id': existing_entry.id, 'message': 'Entry already exists'}

            # Entry doesn't exist, add a new one
            new_entry = Accounting(**data)
            session.add(new_entry)
            session.commit()
            logger.debug("added new item: %s", new_entry)
            return {'id': new_entry.id, 'message': 'Entry added successfully'}

        except Exception as e:
            session.rollback()
            logger.error(str(e))
            return {'error': str(e)}, 500
    
    @staticmethod
    def add_accounting():
        data = request.json

        if isinstance(data, list):
            added_entries = [AccountingAPI._add_single_entry(entry) for entry in data]
            added_entries = [entry for entry in added_entries if 'id' in entry]
            if added_entries:
                ids = [entry['id'] for entry in added_entries]
                return jsonify({'message': 'Entries added successfully', 'added_entries': ids}), 201
            else:
                return jsonify({'error': 'All entries failed to add'}), 500
        else:
            return jsonify(AccountingAPI._add_single_entry(data)), 201
        

    @staticmethod
    def get_accounting_by_timeframe(start_date, end_date):
        try:
            # Validate format
            start = datetime.strptime(start_date, DATE_FORMAT)
            end = datetime.strptime(end_date, DATE_FORMAT)
            logger.debug("Get data by timeframe start: %s, end: %s", start, end)
        except ValueError:
            return jsonify({'error': 'Invalid date format. Please use DD-MM-YYYY'}), 400    

        accounting = session.query(Accounting).filter(
            Accounting.transaction_date.between(start, end)
        ).all()

        total_expenses = 0
        total_income = 0
        entries = []
        for entry in accounting:
            amount = entry.amount
            if amount < 0:
                total_expenses += amount
            elif amount > 0:
                total_income += amount

            entries.append({
                'id': entry.id,
                'date': entry.date.strftime(DATE_FORMAT),
                'transaction_date': entry.transaction_date.strftime(DATE_FORMAT),
                'amount': amount,
                'reference': entry.reference
            })

        return jsonify({
            'entries': entries,
            'total_expenses': total_expenses,
            'total_income': total_income
        })

    @staticmethod
    def add_total_balance():
        data = request.json
        if not data:
            return jsonify({'error': 'Request must not be empty, expected {''total'': 12345 }'}), 400

        try:
            date_str = data['date']
            date_obj = datetime.strptime(date_str, DATE_FORMAT)
            data['date']=date_obj
            data['total'] = data['total'].replace(",", ".")
            existing_entry = session.query(AccountingTotal).filter_by(
                date=data['date'],
            ).first()

            if existing_entry:
                setattr(existing_entry, 'total', data['total'])
                session.commit()
                return jsonify({'message': 'Totals updated successfully'}), 200
            else:
                # Entry doesn't exist, add a new one
                new_entry = AccountingTotal(**data)
                session.add(new_entry)
                session.commit()
                logger.debug("added new item: %s", new_entry)
                return {'id': new_entry.id, 'message': 'Entry added successfully'}

        except Exception as e:
            session.rollback()
            logger.error(str(e))
            return {'error': str(e)}, 500

    @staticmethod    
    def get_total_balance():
        totals = session.query(AccountingTotal).all()
        return jsonify([{
            'id': total.id,
            'date': total.date.strftime(DATE_FORMAT),
            'total': total.total,
        }for total in totals]) 
    
    @staticmethod    
    def get_current_total_balance():
        last_accounting = session.query(AccountingTotal).order_by(desc(AccountingTotal.date)).first()
        return jsonify({
            'id': last_accounting.id,
            'date': last_accounting.date.strftime(DATE_FORMAT),
            'total': last_accounting.total,
        })


    # only available in debug mode    
    @staticmethod
    def delete_all_accounting(enabled=False):
        if not enabled:
            return jsonify({'error': 'No data given'}), 400

        try:
            session.query(Accounting).delete()
            session.commit()
            return jsonify({'message': 'All accounting data deleted successfully'}), 200
        except Exception as e:
            session.rollback()
            return jsonify({'error': str(e)}), 500