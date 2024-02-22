from flask import Flask, request
from flask_cors import CORS
from api.expense_api import ExpenseAPI
from api.income_api import IncomeAPI
from api.accounting_api import AccountingAPI

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Routes for expenses
@app.route('/expenses', methods=['GET'])
def get_expenses():
    return ExpenseAPI.get_expenses()

@app.route('/expenses', methods=['POST'])
def add_expense():
    return ExpenseAPI.add_expense()

@app.route('/expenses/<expense_id>', methods=['PUT'])
def update_expense(expense_id):
    return ExpenseAPI.update_expense(expense_id)

@app.route('/expenses/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    return ExpenseAPI.delete_expense(expense_id)

# Routes for income
@app.route('/income', methods=['GET'])
def get_income():
    return IncomeAPI.get_income()

@app.route('/income', methods=['POST'])
def add_income():
    return IncomeAPI.add_income()

@app.route('/income/<income_id>', methods=['PUT'])
def update_income(income_id):
    return IncomeAPI.update_income(income_id)

@app.route('/income/<income_id>', methods=['DELETE'])
def delete_income(income_id):
    return IncomeAPI.delete_income(income_id)

# Routes for accounting
@app.route('/accounting', methods=['GET'])
def get_accounting():
    return AccountingAPI.get_accounting()

# Define route for getting accounting data by timeframe
@app.route('/accounting/timeframe', methods=['GET'])
def get_accounting_by_timeframe():
    # Extract start_date and end_date from query parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Call the get_accounting_by_timeframe method from AccountingAPI
    return AccountingAPI.get_accounting_by_timeframe(start_date, end_date)

@app.route('/accounting', methods=['POST'])
def add_accounting():
    return AccountingAPI.add_accounting()

@app.route('/accounting', methods=['DELETE'])
def delete_all_accounting():
    return AccountingAPI.delete_all_accounting(enabled=True)

@app.route('/accounting/total', methods=['POST'])
def add_total_balance():
    return AccountingAPI.add_total_balance()

@app.route('/accounting/total', methods=['GET'])
def get_total_balance():
    return AccountingAPI.get_total_balance()

@app.route('/accounting/total/current', methods=['GET'])
def get_current_total_balance():
    return AccountingAPI.get_current_total_balance()

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
