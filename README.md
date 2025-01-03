# Points Management API

## Overview

The Points Management API is a REST API that tracks points for a user across multiple payers. It supports adding, spending, and fetching points balances.

## Features

- **Add Points**: Add points from a specific payer with a timestamp.
- **Spend Points**: Deduct points across payers, adhering to FIFO rules.
- **Fetch Balances**: View the current balance for each payer.

---

## Requirements

### Prerequisites

- **Python 3.8+**: Ensure Python is installeds.
- **Pip**: Python's package manager (comes with Python installations).

---

## Setup

### Install Dependencies

1. Clone this repository or download the code files.
2. Open a terminal and navigate to the project directory.
3. Install Flask by running:
   
   pip install flask

## USAGE

1. Make sure you are in project directory
2. start the server by running
   
   python app.py

NOTE: If you get a message at this point saying flask not installed. Follow these steps:
run this on your terminal 
   
   python - m venv env
   
   source env/bin/activate
   
   pip install flask
   
Now try running python app.py again

4. The API will be accessible at http://localhost:8000

## TESTING

1.  Open another window in terminal and you can run these curl commands one by one

### add.

curl -X POST http://localhost:8000/add -H "Content-Type: application/json" -d '{"payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z"}'

curl -X POST http://localhost:8000/add -H "Content-Type: application/json" -d '{"payer": "UNILEVER", "points": 200, "timestamp": "2022-10-31T11:00:00Z"}'

curl -X POST http://localhost:8000/add -H "Content-Type: application/json" -d '{"payer": "DANNON", "points": -200, "timestamp": "2022-10-31T15:00:00Z"}'

curl -X POST http://localhost:8000/add -H "Content-Type: application/json" -d '{"payer": "MILLER COORS", "points": 10000, "timestamp": "2022-11-01T14:00:00Z"}'

curl -X POST http://localhost:8000/add -H "Content-Type: application/json" -d '{"payer": "DANNON", "points": 1000, "timestamp": "2022-11-02T14:00:00Z"}'

### spend.

curl -X POST http://localhost:8000/spend -H "Content-Type: application/json" -d '{"points": 5000}'

expected output -
[
{ "payer": "DANNON", "points": -100 },
{ "payer": "UNILEVER", "points": -200 },
{ "payer": "MILLER COORS", "points": -4700 }
]

### balance.

curl -X GET http://localhost:8000/balance

expected output -
{
"DANNON": 1000,
"MILLER COORS": 5300,
"UNILEVER": 0,
}
