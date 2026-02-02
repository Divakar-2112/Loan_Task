from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy() 

class Loan(db.Model): # database table create
    id = db.Column(db.Integer,primary_key=True)
    applicant_name = db.Column(db.String(100),nullable=False)
    amount = db.Column(db.Float,nullable=False)
    tenure_months = db.Column(db.Integer,nullable=False)
    status = db.Column(db.Enum('Pending', 'Approved', 'Rejected', name='loan_status'), default='Pending', nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)