# RiskLens

**Open‑Source Credit‑Risk Analytics with Real‑World, Privacy‑Friendly Signals**

RiskLens is a modular, GitHub-ready data analytics toolkit that flags high-risk loan accounts using only publicly available or bank-native signals—no direct income data or PII required.

## 🚀 Key Features
- **Privacy-First:** No PII or income tracking—uses only signals banks already collect or publicly accessible proxies.
- **Extensible & Practical:** Drop-in real data connectors; easy plugin of new proxy features.
- **Clear, Modular Code:** Each stage (ETL, features, modeling, explainability) lives in its own folder—ideal for contributions.
- **Demo-Ready:** Comes with a Jupyter notebook using LendingClub data and a live Streamlit app.

## 🛠️ Core Pipeline & Components
- **Data Ingestion & Simulation:**
  - Public datasets (LendingClub, UCI Credit Card)
  - Modular connectors for bank logs, open-banking CSVs, telecom APIs
- **Feature Engineering Library:**
  - Pre-built transformers for DPD, utilization, transaction-burst detection
  - Easy plugin of custom “proxy” signals (e.g., utility-bill scraper)
- **Modeling Suite:**
  - Baseline: Logistic Regression (L1/L2)
  - Advanced: XGBoost/LightGBM, 1D-CNN on balance time series
  - Built-in cross-validation & hyperparameter tuner
- **Explainability & Monitoring:**
  - SHAP explanations
  - Drift detection for feature-distribution shifts
- **Interactive Dashboard:**
  - Streamlit/React UI: portfolio heatmap, per-borrower “risk radar”, time-slider
- **Alert Engine & Playbooks:**
  - Configurable triggers (e.g., risk score > 0.7)
  - Auto-generate “next best action” suggestions

## 📂 Project Structure
```
RiskLens/
│
├── data_ingestion/         # Data loaders, connectors, and simulators
│   ├── public_datasets/    # Scripts for LendingClub, UCI, etc.
│   └── connectors/         # Bank logs, open banking, telecom APIs
│
├── feature_engineering/    # Feature transformers for all signals
│   ├── payment_behavior.py
│   ├── utilization.py
│   ├── account_activity.py
│   ├── product_signals.py
│   └── proxy_signals.py
│
├── modeling/               # Baseline and advanced models
│   ├── logistic_regression.py
│   ├── xgboost_model.py
│   ├── lgbm_model.py
│   └── sequence_models.py
│
├── explainability/         # SHAP, drift detection, monitoring
│   ├── shap_explain.py
│   └── drift_detection.py
│
├── dashboard/              # Streamlit/React UI
│   ├── app.py
│   └── components/
│
├── alert_engine/           # Triggers and playbooks
│   ├── triggers.py
│   └── actions.py
│
├── notebooks/              # Demo Jupyter notebooks
│   └── demo_lendingclub.ipynb
│
├── tests/                  # Unit and integration tests
│
├── requirements.txt
├── README.md
└── setup.py
```

## 🧩 Contributing
- Fork the repo and create a feature branch.
- Add new connectors, features, or models as modular scripts.
- Write tests for your code in the `tests/` folder.
- Submit a pull request with a clear description.

## 📈 Demo
- Run the Jupyter notebook in `notebooks/` for a quick demo using public data.
- Launch the Streamlit dashboard with `streamlit run dashboard/app.py`.

## 📣 Community Hooks
- Add your region’s macro data adapter
- Build a new proxy-signal plugin

## License
MIT 
