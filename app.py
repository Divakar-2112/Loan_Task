from urllib import response
from flask import Flask,request,jsonify
from models import db,Loan
from datetime import datetime

app = Flask(__name__)

# ================================================== Database Config ==================================================

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///loans.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()

# ================================================== Error Handling Function ==================================================

def bad_request(message):
    return jsonify({"error":message}),400

def not_found(message):
    return jsonify({"error":message}),404

def server_error(message='Internal Server Error'):
    return jsonify({"error":message}),500

# ================================================== Routes ==================================================

# Apply for Loan

@app.route('/api/loans',methods=['POST'])

def apply_loan():
    try:
        data = request.json
        if not data:
            return bad_request("JSON data is required")
        required_fields = ['applicant_name','amount','tenure_months']
        for field in required_fields:
            if field not in data:
                return bad_request(f"{field} is required")
        if data["amount"] <= 0:
            return bad_request("Amount must be positive")
        if int(data["tenure_months"]) <= 0:
            return bad_request("Tenure must be positive")
        loan = Loan(
            applicant_name=data['applicant_name'],
            amount=data['amount'],
            tenure_months=data['tenure_months']
        )
        db.session.add(loan)
        db.session.commit()
        return jsonify({
            "message": "Loan applied successfully", "loan": loan.id }),201
    except Exception as e:
        return server_error(str(e))
    
# Approve Loan 
@app.route('/api/loans/<int:loan_id>/approve',methods=['PATCH'])

def approve_loan(loan_id):
    try:
        loan = Loan.query.get(loan_id)
        if not loan:
            return not_found("Loan application not found")
        if loan.status != 'Pending':
            return bad_request("Only pending loans can be approved")
        loan.status = 'Approved'
        loan.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message":"Loan approved successfully"}),200
    except Exception as e:
        return server_error(str(e))

# Reject Loan
@app.route('/api/loans/<int:loan_id>/reject',methods=['PATCH'])

def reject_loan(loan_id):
    try:
        loan = Loan.query.get(loan_id)
        if not loan:
            return not_found("Loan application not found")
        if loan.status != 'Pending':
            return bad_request("Only pending loans can be rejected")
        loan.status = 'Rejected'
        loan.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"message":"Loan rejected successfully"}),200
    except Exception as e:
        return server_error(str(e))
    

# Get Loan 
@app.route('/api/loans/<int:loan_id>',methods=['GET'])

def get_loan(loan_id):
    try:
        loan = Loan.query.get(loan_id)
        if not loan:
            return not_found("Loan application not found")
        return jsonify({
            "id": loan.id,
            "applicant_name": loan.applicant_name,
            "amount": loan.amount,
            "tenure_months": loan.tenure_months,
            "status": loan.status,
            "created_at": loan.created_at,
            "updated_at": loan.updated_at
        }),200
    except Exception as e:
        return server_error(str(e))
    
# Get All Loans
@app.route('/api/loans',methods=['GET'])

def get_loans():
    try:
        loans = Loan.query.all()
        result = []
        for loan in loans:
            result.append({
                "id": loan.id,
                "applicant_name": loan.applicant_name,
                "amount": loan.amount,
                "tenure_months": loan.tenure_months,
                "status": loan.status,
                "created_at": loan.created_at,
                "updated_at": loan.updated_at
            })
        return jsonify(result),200
    except Exception as e:
        return server_error(str(e))
    
    
   
app.run(debug=True)
