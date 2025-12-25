
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RiskLens.modeling.risk_engine import RiskEngine

def test_income_impact():
    engine = RiskEngine()
    
    # Base profile
    base_profile = {
        "id_res_status": "Indian",
        "prof_geo_risk_score": "Low",
        "fin_existing_emi": 0,
        "fin_lti_ratio": 0.1,
        "fin_documented_income_verified": True,
        "emp_employer_type": "Salaried",
        "ext_cibil_score": 750,
        "beh_past_emi_bounces": 0,
        "ext_previous_npa": False
    }

    # Test Case 1: Low Income
    low_profile = base_profile.copy()
    low_profile["fin_declared_income"] = 250000
    res_low = engine.evaluate(low_profile)
    print(f"Low Income (2.5L) Score: {res_low['risk_score']}")
    
    # Test Case 2: High Income
    high_profile = base_profile.copy()
    high_profile["fin_declared_income"] = 2000000
    res_high = engine.evaluate(high_profile)
    print(f"High Income (20L) Score: {res_high['risk_score']}")

    # Verification
    diff = res_high['risk_score'] - res_low['risk_score']
    print(f"Score Difference: {diff}")
    
    if diff >= 25: # -10 for low, +15 for high = 25 point swing
        print("SUCCESS: Income tiers are working correctly.")
    else:
        print("FAILURE: Score difference is insufficient.")

if __name__ == "__main__":
    test_income_impact()
