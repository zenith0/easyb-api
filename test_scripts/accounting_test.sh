#!/bin/bash

# Function to create accounting data
create_accounting_data() {
    echo "Creating accounting data..."
    # Create accounting data
    curl -X POST -H "Content-Type: application/json" -d '{
        "date": "2024-02-10",
        "transaction_date": "2024-02-10",
        "amount": "100.00",
        "reference": "Test entry 1"
    }' http://localhost:5000/accounting
    echo "Accounting entry 1 created"

    curl -X POST -H "Content-Type: application/json" -d '{
        "date": "2024-02-11",
        "transaction_date": "2024-02-11",
        "amount": "150.00",
        "reference": "Test entry 2"
    }' http://localhost:5000/accounting
    echo "Accounting entry 2 created"
}

# Function to retrieve accounting data for a certain timeframe
retrieve_data_for_timeframe() {
    echo "Retrieving accounting data for timeframe..."
    # Example: Retrieve data for the month of February 2024
    curl http://localhost:5000/accounting/timeframe?start_date=2024-02-01\&end_date=2024-02-29
}

# Function to retrieve all accounting entries
retrieve_all_entries() {
    echo "Retrieving all accounting entries..."
    curl http://localhost:5000/accounting
}

# Function to delete all accounting entries
delete_all_entries() {
    echo "Deleting all accounting entries..."
    curl -X DELETE http://localhost:5000/accounting
}

# Main function
main() {
    create_accounting_data
    retrieve_data_for_timeframe
    retrieve_all_entries
    # delete_all_entries
}

# Run the main function
main
