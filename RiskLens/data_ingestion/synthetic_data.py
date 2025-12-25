import random
import datetime
import numpy as np
import pandas as pd
import uuid

class RiskProfileGenerator:
    def __init__(self, seed=None):
        if seed:
            random.seed(seed)
            np.random.seed(seed)

    def _generate_pan(self):
        chars = "ABCDE"
        nums = "0123456789"
        return "".join(random.choices(chars, k=5)) + "".join(random.choices(nums, k=4)) + random.choice(chars)

    def _generate_aadhaar(self):
        return "XXXX-XXXX-" + "".join(random.choices("0123456789", k=4))

    def generate_profile(self):
        # Identity anchors
        age = random.randint(21, 65)
        dob = datetime.date.today() - datetime.timedelta(days=age*365)
        
        profile = {
            "id_pan": self._generate_pan(),
            "id_aadhaar": self._generate_aadhaar(),
            "id_dob": dob.isoformat(),
            "id_age": age,
            "id_res_status": random.choices(["Indian", "NRI"], weights=[0.95, 0.05])[0],

            # Financial capacity
            "fin_declared_income": int(np.random.lognormal(13, 0.5)), # ~440k median
            "fin_documented_income_verified": random.choice([True, True, False]),
            "fin_avg_monthly_balance": int(np.random.lognormal(10, 1)),
            "fin_income_stability": random.choice(["Stable", "Variable", "Seasonal"]),
            "fin_existing_emi": int(np.random.exponential(5000)),
            "fin_dependents": random.randint(0, 4),
            
            # Employment stability
            "emp_occupation": random.choice(["Salaried", "Self-Employed", "Business", "Professional"]),
            "emp_employer_type": random.choice(["Govt", "PSU", "MNC", "Private", "SME", "Unemployed"]),
            "emp_tenure_years": random.randint(0, 20),
            
            # Behavioural banking data
            "beh_past_emi_bounces": np.random.poisson(0.2),
            "beh_overdraft_instances": np.random.poisson(0.1),
            "beh_avg_credit_utilization": random.uniform(0, 1.0),
            "beh_cash_withdrawal_ratio": random.uniform(0, 1.0), # vs digital
            "beh_spending_shock": random.choice([False, False, False, True]), # Sudden change
            
            # External credit ecosystem
            "ext_cibil_score": int(np.clip(np.random.normal(750, 50), 300, 900)),
            "ext_open_credit_accounts": random.randint(0, 10),
            "ext_total_sanctioned_limit": int(np.random.exponential(100000)),
            "ext_credit_history_years": random.randint(1, 15),
            "ext_inquiries_last_6m": np.random.poisson(0.5),
            "ext_previous_npa": random.choices([True, False], weights=[0.02, 0.98])[0],
            
            # Asset and collateral signals
            "asset_collateral_value": int(np.random.exponential(500000)) if random.random() > 0.7 else 0,
            "asset_residence_type": random.choice(["Owned", "Rented", "Parental"]),
            
            # Customer profile risk flags
            "prof_address_changes_last_3y": np.random.poisson(0.3),
            "prof_geo_risk_score": random.choice(["Low", "Medium", "High"]),
            
            # Account-level operational metadata
            "ops_tenure_months": random.randint(1, 120),
            "ops_active_products": random.randint(1, 5),
            "ops_savings_consistency": random.uniform(0, 1) # 1 is very consistent
        }
        
        # Derived fields for logic
        profile["fin_lti_ratio"] = (profile["fin_existing_emi"] * 12) / (profile["fin_declared_income"] + 1)
        
        return profile

    def generate_batch(self, n=100):
        return pd.DataFrame([self.generate_profile() for _ in range(n)])

if __name__ == "__main__":
    gen = RiskProfileGenerator()
    df = gen.generate_batch(5)
    print(df.head())
