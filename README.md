# Financial Management System API

The Financial Management System API provides endpoints to manage expenses and income data in a financial system. This API is built using Flask and SQLAlchemy and allows users to perform CRUD operations on expenses and income items.

## Base URL

The base URL for the API is `http://localhost:5000`.

## Endpoints

### 1. Get Expenses

- **Endpoint**: `/expenses`
- **Method**: `GET`
- **Description**: Retrieves all expenses.
- **Response**:
  - HTTP Status Code: `200 OK`
  - Body: JSON array containing details of all expenses.

### 2. Add Expense

- **Endpoint**: `/expenses`
- **Method**: `POST`
- **Description**: Adds a new expense.
- **Request Body**:
  - Format: JSON
  - Fields:
    - `id`: (optional) Unique identifier for the expense. If not provided, a random ID will be generated.
    - `reference`: Reference or description of the expense.
    - `amount`: Amount of the expense.
    - `matcher`: Matcher for the expense.
- **Response**:
  - HTTP Status Code: `201 Created`
  - Body: JSON containing a message confirming the addition of the expense and the ID of the newly added expense.

### 3. Update Expense

- **Endpoint**: `/expenses/<expense_id>`
- **Method**: `PUT`
- **Description**: Updates an existing expense.
- **Path Parameter**:
  - `expense_id`: ID of the expense to be updated.
- **Request Body**:
  - Format: JSON
  - Fields: (optional)
    - `reference`: Updated reference or description of the expense.
    - `amount`: Updated amount of the expense.
    - `matcher`: Updated matcher for the expense.
- **Response**:
  - HTTP Status Code: `200 OK`
  - Body: JSON containing a message confirming the successful update of the expense.

### 4. Delete Expense

- **Endpoint**: `/expenses/<expense_id>`
- **Method**: `DELETE`
- **Description**: Deletes an existing expense.
- **Path Parameter**:
  - `expense_id`: ID of the expense to be deleted.
- **Response**:
  - HTTP Status Code: `200 OK`
  - Body: JSON containing a message confirming the successful deletion of the expense.

### 5. Get Income

- **Endpoint**: `/income`
- **Method**: `GET`
- **Description**: Retrieves all income items.
- **Response**:
  - HTTP Status Code: `200 OK`
  - Body: JSON array containing details of all income items.

### 6. Add Income

- **Endpoint**: `/income`
- **Method**: `POST`
- **Description**: Adds a new income item.
- **Request Body**:
  - Format: JSON
  - Fields:
    - `id`: (optional) Unique identifier for the income item. If not provided, a random ID will be generated.
    - `reference`: Reference or description of the income item.
    - `amount`: Amount of the income item.
    - `matcher`: Matcher for the income item.
- **Response**:
  - HTTP Status Code: `201 Created`
  - Body: JSON containing a message confirming the addition of the income item and the ID of the newly added income item.

### 7. Update Income

- **Endpoint**: `/income/<income_id>`
- **Method**: `PUT`
- **Description**: Updates an existing income item.
- **Path Parameter**:
  - `income_id`: ID of the income item to be updated.
- **Request Body**:
  - Format: JSON
  - Fields: (optional)
    - `reference`: Updated reference or description of the income item.
    - `amount`: Updated amount of the income item.
    - `matcher`: Updated matcher for the income item.
- **Response**:
  - HTTP Status Code: `200 OK`
  - Body: JSON containing a message confirming the successful update of the income item.

### 8. Delete Income

- **Endpoint**: `/income/<income_id>`
- **Method**: `DELETE`
- **Description**: Deletes an existing income item.
- **Path Parameter**:
  - `income_id`: ID of the income item to be deleted.
- **Response**:
  - HTTP Status Code: `200 OK`
  - Body: JSON containing a message confirming the successful deletion of the income item.

## Data Models

The API uses two main data models:

### Expense

- **Fields**:
  - `id`: Unique identifier for the expense.
  - `reference`: Reference or description of the expense.
  - `amount`: Amount of the expense.
  - `matcher`: Matcher for the expense.

### Income

- **Fields**:
  - `id`: Unique identifier for the income item.
  - `reference`: Reference or description of the income item.
  - `amount`: Amount of the income item.
  - `matcher`: Matcher for the income item.

## Usage

1. Start the Flask application by running the provided code.
2. Use the specified endpoints to interact with the API using appropriate HTTP methods and request bodies.

## Dependencies

- Flask: Web framework for building APIs in Python.
- SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM)

 library for Python.
- psycopg2: PostgreSQL adapter for Python.

---

This API documentation provides details about the endpoints, request and response formats, data models, and usage instructions for the Financial Management System API. Use this document as a reference to understand and utilize the API for managing financial data.