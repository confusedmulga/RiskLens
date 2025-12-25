# RiskLens

RiskLens is a modular credit scoring engine built in Python. It assesses borrower risk by analyzing behavioral patterns and alternative data instead of just traditional methods. The system uses a decoupled Risk Engine that runs both heuristic rules and Machine Learning classifiers like XGBoost.

It includes a dynamic data pipeline for reading bank statements, a real time Streamlit dashboard for underwriters, and integration with SHAP values to explain why a specific score was given.

### Key Features
*   **Privacy First Architecture**: Calculates risk without storing sensitive personal data.
*   **Dynamic Risk Engine**: Uses configurable logic to combine credit data with behavioral signals.
*   **Interactive Dashboard**: A web interface for simulating profiles and visualizing risk factors.
*   **Income Verification**: Automatically checks declared income against uploaded bank statements.
*   **Explainable AI**: Shows exactly which factors contributed to the risk score using SHAP.

### Data Signals Used
The system uses data from four main categories:

**Financial Capacity**
*   Annual Income (Verified via bank statement)
*   Existing EMI Burden
*   Loan to Income Ratio

**Behavioral History**
*   CIBIL Score
*   Past EMI Bounces
*   Credit Utilization Ratio
*   NPA History

**Employment Stability**
*   Employer Type (Government or Private)
*   Job Tenure
*   Occupation Category

**Identity and Demographics**
*   Residential Status
*   Age
*   Geo Risk Score

## Project Structure
```
RiskLens/
│
├── data_ingestion/         # Scripts for loading and parsing data
├── feature_engineering/    # Logic for creating risk signals
├── modeling/               # Risk scoring models and logic
├── explainability/         # SHAP and drift detection tables
├── dashboard/              # Streamlit web application
├── alert_engine/           # Triggers for high risk accounts
├── notebooks/              # Jupyter notebooks for demos
└── tests/                  # Unit tests
```

## How to Run
1.  Install dependencies:
    `pip install -r RiskLens/requirements.txt`
2.  Run the dashboard:
    `streamlit run dashboard/app.py`
