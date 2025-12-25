import sys
import os
import pandas as pd

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RiskLens.data_ingestion.synthetic_data import RiskProfileGenerator
from RiskLens.modeling.risk_engine import RiskEngine

def test_logic():
    print("Initializing Generator...")
    gen = RiskProfileGenerator(seed=42)
    
    print("Generating Profile...")
    profile = gen.generate_profile()
    print("Profile Generated:")
    for k, v in profile.items():
        print(f"  {k}: {v}")
        
    print("\nInitializing Engine...")
    engine = RiskEngine()
    
    print("Evaluating Profile...")
    analysis = engine.evaluate(profile)
    
    print("\nAnalysis Result:")
    for k, v in analysis.items():
        if k == 'drivers':
            print("  Drivers:")
            for d in v:
                print(f"    {d['desc']} ({d['impact']})")
        else:
            print(f"  {k}: {v}")

    # Basic Assertions
    assert 0 <= analysis['risk_score'] <= 100, "Score out of range"
    assert 0 <= analysis['prob_default'] <= 1, "Prob Default out of range"
    assert analysis['rec_limit'] >= 0, "Limit negative"
    
    print("\nVerification Successful!")

if __name__ == "__main__":
    test_logic()
