from RiskLens.modeling.risk_engine import RiskEngine


def _base_profile():
    return {
        "id_res_status": "Indian",
        "prof_geo_risk_score": "Low",
        "fin_declared_income": 600000,
        "fin_documented_income_verified": True,
        "fin_existing_emi": 5000,
        "fin_lti_ratio": 0.1,
        "emp_employer_type": "Private",
        "beh_past_emi_bounces": 0,
        "ext_previous_npa": False,
    }


def test_cibil_750_gets_excellent_bonus():
    engine = RiskEngine()

    profile_749 = _base_profile() | {"ext_cibil_score": 749}
    profile_750 = _base_profile() | {"ext_cibil_score": 750}

    result_749 = engine.evaluate(profile_749)
    result_750 = engine.evaluate(profile_750)

    assert result_750["risk_score"] > result_749["risk_score"]
    assert any(d["factor"] == "CIBIL Score" for d in result_750["drivers"])


def test_limit_range_never_inverted_for_low_scores():
    engine = RiskEngine()
    profile = _base_profile() | {
        "ext_cibil_score": 300,
        "beh_past_emi_bounces": 4,
        "ext_previous_npa": True,
    }

    result = engine.evaluate(profile)

    assert result["min_limit"] <= result["max_limit"]
    assert result["min_limit"] <= result["rec_limit"] <= result["max_limit"]
