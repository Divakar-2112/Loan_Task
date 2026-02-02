# Loan Project

# Feature Overview

1. Apply Loan
2. View Loan 
3. View All Loans
4. Approve Loan
5. Reject Loan

# Technologies Used

1. Python
2. Flask
3. Flask-SQLAlchemy
4. SQLite Database

# API Endpoints

Method | Endpoint        | Description
POST   | /api/loans         | Apply for a new loan
GET    | /api/loans/<id>    | View a specific loan
GET    | /api/loans         | View all loans
PATCH    | /api/loans/<id>/approve | Approve a loan
PATCH    | /api/loans/<id>/reject  | Reject a loan

# Sample Request (POST)
```json
{
    "applicant_name": "Diva",
    "amount": 5000,
    "tenure_months": 12,
}
```

# Run the Project
``` 
pip install -r requirements.txt
python app.py

```