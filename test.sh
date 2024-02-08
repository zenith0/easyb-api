#!/bin/bash

# Set the base URL of your Flask app
BASE_URL="http://127.0.0.1:5000"

# Function to generate a random ID
generate_random_id() {
    uuidgen | cut -d'-' -f 1
}

# Function to create test data
create_test_data() {
    echo "Creating test data..."
    # Create an expense with a predefined ID
    expense_id=$(generate_random_id)
    expense_response=$(curl -X POST -H "Content-Type: application/json" -d '{"id": "'"$expense_id"'", "reference": "Test expense", "amount": "100", "matcher": "Test matcher"}' -w "%{http_code}" -o /dev/null $BASE_URL/expenses)
    if [ $expense_response -eq 201 ]; then
        echo "Expense created successfully with ID: $expense_id"
    else
        echo "Failed to create expense. HTTP response code: $expense_response"
        exit 1
    fi

    # Create an income item with a predefined ID
    income_id=$(generate_random_id)
    income_response=$(curl -X POST -H "Content-Type: application/json" -d '{"id": "'"$income_id"'", "reference": "Test income", "amount": "500", "matcher": "Test matcher"}' -w "%{http_code}" -o /dev/null $BASE_URL/income)
    if [ $income_response -eq 201 ]; then
        echo "Income created successfully with ID: $income_id"
    else
        echo "Failed to create income. HTTP response code: $income_response"
        exit 1
    fi
    echo "Test data created successfully."
}

# Function to read test data
read_test_data() {
    echo "Reading test data..."
    # Read expenses
    echo "Expenses:"
    curl $BASE_URL/expenses
    # Read income
    echo "Income:"
    curl $BASE_URL/income
}

# Function to update test data
update_test_data() {
    echo "Updating test data..."
    # Update the created expense with new amount
    expense_update_response=$(curl -X PUT -H "Content-Type: application/json" -d '{"amount": "150"}' -w "%{http_code}" -o /dev/null $BASE_URL/expenses/$expense_id)
    if [ $expense_update_response -eq 200 ]; then
        echo "Expense updated successfully"
    else
        echo "Failed to update expense. HTTP response code: $expense_update_response"
    fi

    # Update the created income item with new amount
    income_update_response=$(curl -X PUT -H "Content-Type: application/json" -d '{"amount": "600"}' -w "%{http_code}" -o /dev/null $BASE_URL/income/$income_id)
    if [ $income_update_response -eq 200 ]; then
        echo "Income updated successfully"
    else
        echo "Failed to update income. HTTP response code: $income_update_response"
    fi
}

# Function to delete test data
delete_test_data() {
    echo "Deleting test data..."
    # Delete the created expense
    expense_delete_response=$(curl -X DELETE -w "%{http_code}" -o /dev/null $BASE_URL/expenses/$expense_id)
    if [ $expense_delete_response -eq 200 ]; then
        echo "Expense deleted successfully"
    else
        echo "Failed to delete expense. HTTP response code: $expense_delete_response"
    fi

    # Delete the created income item
    income_delete_response=$(curl -X DELETE -w "%{http_code}" -o /dev/null $BASE_URL/income/$income_id)
    if [ $income_delete_response -eq 200 ]; then
        echo "Income deleted successfully"
    else
        echo "Failed to delete income. HTTP response code: $income_delete_response"
    fi
    echo "Test data deleted successfully."
}

# Main function
main() {
    # Create test data
    create_test_data
    # Read test data
    read_test_data
    # Update test data
    update_test_data
    # Read updated test data
    read_test_data
    # Delete test data
    delete_test_data
}

# Run the main function
main

