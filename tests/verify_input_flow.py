import sys
import os
import pandas as pd
import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RiskLens.modeling.risk_engine import RiskEngine

def test_input_flow():
    print("Testing Input Data Flow...")
    
    # Simulate data from the Input Screen
    # This matches the dictionary construction in app.py
    dob = datetime.date(1990, 1, 1)
    income = 1200000
    total_emi = 30000
    
    profile_data = {
        "id_pan": "ABCDE1234F",
        "id_aadhaar": "1234",
        "id_res_status": "Indian",
        "id_age": (pd.Timestamp.now().date() - dob).days // 365,
        
        "fin_declared_income": income,
        "fin_documented_income_verified": True,
        "fin_existing_emi": total_emi,
        "fin_lti_ratio": (total_emi * 12) / (income + 1),
        "fin_dependents": 2,
        
        "emp_occupation": "Salaried - Pvt",
        "emp_employer_type": "Private",
        "emp_tenure_years": 5,
        
        "ext_cibil_score": 780,
        "ext_open_credit_accounts": 3,
        "ext_previous_npa": False,
        
        "beh_past_emi_bounces": 0,
        "beh_avg_credit_utilization": 0.3,
        
        "asset_collateral_value": 0,
        "prof_geo_risk_score": "Low"
    }
    
    print("Input Profile Constructed.")
    
    # Run Engine
    engine = RiskEngine()
    analysis = engine.evaluate(profile_data)
    
    print("Risk Engine Analysis Result:")
    print(f"  Risk Score: {analysis['risk_score']}")
    print(f"  Rec Limit: {analysis['rec_limit']}")
    
    # Assertions
    assert analysis['risk_score'] > 0, "Risk Score should be positive"
    assert analysis['rec_limit'] > 0, "Rec Limit should be positive for this profile"
    
    print("Verification Successful!")

if __name__ == "__main__":
    test_input_flow()
