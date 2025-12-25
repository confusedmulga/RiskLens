import numpy as np

class RiskEngine:
    def __init__(self):
        pass

    def evaluate(self, profile):
        """
        Evaluates a customer profile and returns risk metrics.
        """
        score = 50  # Base score
        drivers = []

        # --- 1. Identity & Profile (Base Trust) ---
        if profile.get("id_res_status") == "Indian":
            score += 5
            drivers.append({"factor": "Residential Status", "impact": +5, "desc": "Resident Indian"})
        
        if profile.get("prof_geo_risk_score") == "High":
            score -= 10
            drivers.append({"factor": "Geo Risk", "impact": -10, "desc": "High Risk Location"})
        
        # --- 2. Financial Capacity ---
        income = profile.get("fin_declared_income", 0)
        emi = profile.get("fin_existing_emi", 0)
        lti = profile.get("fin_lti_ratio", 0)
        
        # Income Tiers (Annual)
        if income > 1500000:
            score += 15
            drivers.append({"factor": "Income Level", "impact": +15, "desc": "High Income (>15L)"})
        elif income > 1000000:
            score += 10
            drivers.append({"factor": "Income Level", "impact": +10, "desc": "Mid-High Income (>10L)"})
        elif income > 500000:
            score += 5
            drivers.append({"factor": "Income Level", "impact": +5, "desc": "Middle Income (>5L)"})
        elif income < 300000:
            score -= 10
            drivers.append({"factor": "Income Level", "impact": -10, "desc": "Low Income (<3L)"})

        if profile.get("fin_documented_income_verified"):
            score += 10
            drivers.append({"factor": "Income Verification", "impact": +10, "desc": "Documented Income"})
        else:
            score -= 5
            drivers.append({"factor": "Income Verification", "impact": -5, "desc": "Declared Only"})

        if lti > 0.6:
            score -= 15
            drivers.append({"factor": "Loan-to-Income", "impact": -15, "desc": "High Debt Burden (>60%)"})
        elif lti < 0.3:
            score += 10
            drivers.append({"factor": "Loan-to-Income", "impact": +10, "desc": "Low Debt Burden (<30%)"})

        # --- 3. Employment Stability ---
        if profile.get("emp_employer_type") in ["Govt", "PSU"]:
            score += 10
            drivers.append({"factor": "Employment", "impact": +10, "desc": "Govt/PSU Employer"})
        elif profile.get("emp_employer_type") == "Unemployed":
            score -= 20
            drivers.append({"factor": "Employment", "impact": -20, "desc": "Unemployed"})

        # --- 4. Behavioral & History ---
        cibil = profile.get("ext_cibil_score", 0)
        if cibil > 750:
            score += 20
            drivers.append({"factor": "CIBIL Score", "impact": +20, "desc": "Excellent Credit Score"})
        elif cibil < 650:
            score -= 20
            drivers.append({"factor": "CIBIL Score", "impact": -20, "desc": "Poor Credit Score"})

        bounces = profile.get("beh_past_emi_bounces", 0)
        if bounces > 0:
            impact = -5 * bounces
            score += impact
            drivers.append({"factor": "Payment History", "impact": impact, "desc": f"{bounces} EMI Bounces"})

        if profile.get("ext_previous_npa"):
            score -= 50
            drivers.append({"factor": "Critical Flag", "impact": -50, "desc": "Previous NPA"})

        # --- Final Score Clamping ---
        score = max(0, min(100, score))

        # --- Probabilities ---
        # Simple logistic mapping: Score 0 -> High PD, Score 100 -> Low PD
        # Let's say Score 50 is 5% PD. Score 0 is 50% PD. Score 100 is 0.1% PD.
        # This is a heuristic mapping.
        prob_default = 1 / (1 + np.exp((score - 20) / 10))  # Sigmoid-ish
        # Adjusting to make it look realistic
        if score < 30:
            prob_default = 0.4 + (30 - score)/100 # 0.4 to 0.7
        elif score > 80:
            prob_default = 0.01
        else:
            prob_default = 0.05 + (80 - score) * 0.007 # Linear approx between

        prob_repayment = 1.0 - prob_default

        # --- Credit Limit Recommendation ---
        disposable_income = (income / 12) - emi
        if disposable_income < 0:
            rec_limit = 0
            min_limit = 0
            max_limit = 0
        else:
            # Multiplier based on score
            multiplier = score / 10  # e.g., Score 70 -> 7x monthly disposable
            rec_limit = disposable_income * multiplier
            min_limit = disposable_income * 1
            max_limit = disposable_income * (multiplier * 1.5)

        return {
            "risk_score": int(score),
            "prob_default": round(prob_default, 3),
            "prob_repayment": round(prob_repayment, 3),
            "rec_limit": int(rec_limit),
            "min_limit": int(min_limit),
            "max_limit": int(max_limit),
            "drivers": drivers
        }
