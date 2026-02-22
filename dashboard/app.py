import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
import os
import time
import datetime

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RiskLens.modeling.risk_engine import RiskEngine

st.set_page_config(page_title="RiskLens Assessment", layout="wide")

# --- CSS for "Underwriter" Look ---
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        height: 3em;
        font-weight: 600;
    }
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 4px;
        background-color: white;
    }
    .summary-box {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        font-weight: bold;
    }
    .success-box { background-color: #d4edda; color: #155724; }
    .error-box { background-color: #f8d7da; color: #721c24; }
</style>
""", unsafe_allow_html=True)

# --- Session State ---
if 'page' not in st.session_state:
    st.session_state.page = 'input'
if 'profile' not in st.session_state:
    st.session_state.profile = {}
if 'analysis' not in st.session_state:
    st.session_state.analysis = {}

# --- Helper Functions ---
def parse_bank_statement(file):
    """Parses an Excel bank statement with columns: Date, Description, Debit, Credit, Balance."""
    try:
        df = pd.read_excel(file)
        # Normalize headers
        df.columns = [c.strip().title() for c in df.columns]
        required_cols = {'Date', 'Description', 'Debit', 'Credit', 'Balance'}
        
        if not required_cols.issubset(set(df.columns)):
            return False, f"Missing columns. Required: {required_cols}", None
            
        # Basic data cleaning
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        for col in ['Debit', 'Credit', 'Balance']:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        return True, "Parsed successfully", df
    except Exception as e:
        return False, f"Error reading file: {str(e)}", None

def validate_inputs(inputs):
    """Checks if mandatory fields are filled."""
    checks = {
        "Identity": bool(inputs.get('id_pan') and inputs.get('id_aadhaar')),
        "Financial": bool(inputs.get('fin_declared_income') and inputs.get('fin_declared_income') > 0),
        "CIBIL": bool(inputs.get('ext_cibil_score') and inputs.get('ext_cibil_score') > 0),
        "Profile": bool(inputs.get('emp_occupation'))
    }
    return checks

# --- Page 1: Input Screen ---
def render_input_screen():
    st.title("RiskLens Intake Pipeline")
    st.markdown("---")

    # REMOVED st.form wrapper to enable live validation
    # 1. Identity Anchors
    with st.expander("Identity & Regulatory Anchors", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        name = c1.text_input("Applicant Name")
        # Date limits: 18 to 80 years old
        today = datetime.date.today()
        min_dob = today - datetime.timedelta(days=80*365)
        max_dob = today - datetime.timedelta(days=18*365)
        default_dob = today - datetime.timedelta(days=30*365)
        dob = c2.date_input("Date of Birth", value=default_dob, min_value=min_dob, max_value=max_dob)
        pan = c3.text_input("PAN Number", max_chars=10)
        aadhaar = c4.text_input("Aadhaar (Last 4)", max_chars=4)
        
        c1, c2 = st.columns(2)
        res_status = c1.selectbox("Residential Status", ["Indian", "NRI"])
        emp_type = c2.selectbox("Employment Type", ["Salaried", "Self-Employed", "Business", "Professional"])

    # 2. Financial Backbone
    st.subheader("Financial Backbone")
    tab1, tab2 = st.tabs(["CIBIL & Exposure", "Bank Statements"])
    
    with tab1:
        c1, c2, c3 = st.columns(3)
        cibil = c1.number_input("CIBIL Score", 300, 900, 750)
        open_loans = c2.number_input("Existing Active Loans", 0, 20, 0)
        total_emi = c3.number_input("Total Existing EMI (Monthly)", 0, 1000000, 0)
        
        c1, c2 = st.columns(2)
        total_limit = c1.number_input("Total Credit Limit Sanctioned", 0, 10000000, 0)
        npa_flag = c2.checkbox("History of NPA / Settlements?")

    with tab2:
        uploaded_files = st.file_uploader("Upload Bank Statements (PDF/Excel)", accept_multiple_files=True)
        parsing_status = {}
        if uploaded_files:
            st.markdown("### Parsing Status")
            for f in uploaded_files:
                success, msg, _ = parse_bank_statement(f)
                parsing_status[f.name] = success
                if success:
                    st.success(f"✔ {f.name}: {msg}")
                else:
                    st.error(f"✘ {f.name}: {msg}")

    # 3. Customer Profile
    st.subheader("Customer Profile & Stability")
    with st.container():
        c1, c2, c3, c4 = st.columns(4)
        income = c1.number_input("Declared Annual Income", 0, 100000000, 500000)
        occupation = c2.selectbox("Occupation Category", ["Salaried - Pvt", "Salaried - Govt", "Business - Retail", "Business - Mfg", "Professional"])
        tenure = c3.number_input("Years in Current Job/Biz", 0, 50, 2)
        res_years = c4.number_input("Years in Current Residence", 0, 50, 5)
        
        c1, c2, c3 = st.columns(3)
        dependents = c1.number_input("Number of Dependents", 0, 10, 2)
        collateral = c2.number_input("Collateral Value (Optional)", 0, 100000000, 0)
        geo_risk = c3.selectbox("Geo Risk Score", ["Low", "Medium", "High"])

    st.markdown("---")

    # 4. Summary Check Panel & Submit
    c_summary, c_submit = st.columns([2, 1])
    
    with c_summary:
        st.markdown("#### Validation Matrix")
        # Live validation check
        inputs = {
            "id_pan": pan, "id_aadhaar": aadhaar,
            "fin_declared_income": income, "ext_cibil_score": cibil,
            "emp_occupation": occupation
        }
        checks = validate_inputs(inputs)
        
        cols = st.columns(4)
        for i, (k, v) in enumerate(checks.items()):
            color = "green" if v else "red"
            icon = "✔" if v else "✘"
            cols[i].markdown(f"<span style='color:{color}; font-weight:bold'>{k} {icon}</span>", unsafe_allow_html=True)
        
        is_valid = all(checks.values())

    with c_submit:
        st.markdown("<br>", unsafe_allow_html=True)
        # Changed to regular button since we are not in a form anymore
        submit_btn = st.button("GENERATE RISK OUTPUT", disabled=not is_valid)
        if submit_btn:
            if not is_valid:
                st.error("Please fill all mandatory fields.")
            else:
                # Progress Animation
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                steps = ["Validating inputs...", "Parsing bank statements...", "Running risk engine...", "Calculating limits..."]
                for i, step in enumerate(steps):
                    status_text.text(step)
                    progress_bar.progress((i + 1) * 25)
                    time.sleep(0.5)
                
                # Prepare Profile Data
                employer_type = (
                    "Govt" if occupation == "Salaried - Govt"
                    else "Self-Employed" if occupation in ["Business - Retail", "Business - Mfg", "Professional"]
                    else "Private"
                )

                profile_data = {
                    "id_pan": pan,
                    "id_aadhaar": aadhaar,
                    "id_res_status": res_status,
                    "id_age": (pd.Timestamp.now().date() - dob).days // 365,
                    
                    "fin_declared_income": income,
                    
                    # Logic: If Bank Stmt is parsed successfully, we check if it matches declared income.
                    # For this demo, if ANY bank stmt is provided and parsed, we treat it as VERIFIED.
                    # In a real app, we would sum the credits and compare.
                    "fin_documented_income_verified": any(parsing_status.values()) if parsing_status else False,
                    
                    "fin_existing_emi": total_emi,
                    "fin_lti_ratio": (total_emi * 12) / (income + 1),
                    "fin_dependents": dependents,
                    
                    "emp_occupation": occupation,
                    "emp_employer_type": employer_type,
                    "emp_tenure_years": tenure,
                    
                    "ext_cibil_score": cibil,
                    "ext_open_credit_accounts": open_loans,
                    "ext_previous_npa": npa_flag,
                    
                    "beh_past_emi_bounces": 0, # Default for manual entry
                    "beh_avg_credit_utilization": 0.3, # Default
                    
                    "asset_collateral_value": collateral,
                    "prof_geo_risk_score": geo_risk
                }
                
                # Run Engine
                engine = RiskEngine()
                analysis = engine.evaluate(profile_data)
                
                # Update State
                st.session_state.profile = profile_data
                st.session_state.analysis = analysis
                st.session_state.page = 'report'
                st.rerun()

# --- Page 2: Report Screen ---
def render_report_screen():
    # Sidebar Navigation
    st.sidebar.title("RiskLens")
    if st.sidebar.button("← Back to Input"):
        st.session_state.page = 'input'
        st.rerun()
    
    st.sidebar.markdown("### Applicant ID")
    st.sidebar.info(f"PAN: {st.session_state.profile.get('id_pan')}")
    
    # Main Dashboard (Reused Code)
    st.title("Credit Risk Assessment")
    
    analysis = st.session_state.analysis
    profile = st.session_state.profile
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Panel 1: Risk Score Gauge
    with col1:
        st.subheader("Risk Score")
        score = analysis['risk_score']
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [0, 100]},
                'bar': {'color': "black"},
                'steps': [
                    {'range': [0, 50], 'color': "#ff4b4b"},
                    {'range': [50, 75], 'color': "#fca311"},
                    {'range': [75, 100], 'color': "#2b9348"}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': score
                }
            }
        ))
        fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)

    # Panel 2: Probabilities Bar Chart
    with col2:
        st.subheader("Probabilities")
        prob_def = analysis['prob_default']
        prob_rep = analysis['prob_repayment']
        
        fig_bar = go.Figure(data=[
            go.Bar(name='Default', x=['Default'], y=[prob_def], marker_color='#ff4b4b'),
            go.Bar(name='Repayment', x=['Repayment'], y=[prob_rep], marker_color='#2b9348')
        ])
        fig_bar.update_layout(
            yaxis=dict(range=[0, 1], title="Probability"),
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # Panel 3: Recommended Limit Slider
    with col3:
        st.subheader("Credit Limit")
        rec_limit = analysis['rec_limit']
        min_limit = analysis['min_limit']
        max_limit = analysis['max_limit']
        
        fig_limit = go.Figure()
        fig_limit.add_trace(go.Bar(
            x=['Limit'],
            y=[max_limit - min_limit],
            base=[min_limit],
            marker_color='lightgrey',
            name='Safe Range',
            width=0.3
        ))
        fig_limit.add_trace(go.Scatter(
            x=['Limit'],
            y=[rec_limit],
            mode='markers+text',
            marker=dict(color='blue', size=15, symbol='diamond'),
            text=[f"₹{rec_limit:,}"],
            textposition="middle right",
            name='Recommended'
        ))
        fig_limit.update_layout(
            height=300,
            showlegend=False,
            yaxis=dict(title="Amount (₹)"),
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_limit, use_container_width=True)

    # Panel 4: Risk Drivers Waterfall
    with col4:
        st.subheader("Risk Drivers")
        drivers = analysis['drivers']
        if drivers:
            factors = [d['factor'] for d in drivers]
            impacts = [d['impact'] for d in drivers]
            factors = ['Base Score'] + factors + ['Final Score']
            impacts = [50] + impacts + [0]
            measure = ['absolute'] + ['relative'] * (len(drivers)) + ['total']
            
            fig_waterfall = go.Figure(go.Waterfall(
                name = "20", orientation = "v",
                measure = measure,
                x = factors,
                textposition = "outside",
                text = [f"{x:+}" if i > 0 and i < len(impacts)-1 else str(x) for i, x in enumerate(impacts)],
                y = impacts,
                connector = {"line":{"color":"rgb(63, 63, 63)"}},
            ))
            fig_waterfall.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=50, b=20),
                xaxis=dict(tickfont=dict(size=10))
            )
            st.plotly_chart(fig_waterfall, use_container_width=True)
        else:
            st.info("No significant risk drivers identified.")

    # Drill Down Sections
    st.markdown("---")
    st.subheader("Detailed Analysis")
    
    with st.expander("Identity & Demographics"):
        c1, c2, c3 = st.columns(3)
        c1.metric("Age", profile.get('id_age', 'N/A'))
        c2.metric("Residential Status", profile.get('id_res_status', 'N/A'))
        c3.metric("Geo Risk", profile.get('prof_geo_risk_score', 'N/A'))

    with st.expander("Financial Capacity"):
        c1, c2, c3 = st.columns(3)
        c1.metric("Declared Income", f"₹{profile.get('fin_declared_income', 0):,}")
        c2.metric("Existing EMI", f"₹{profile.get('fin_existing_emi', 0):,}")
        c3.metric("LTI Ratio", f"{profile.get('fin_lti_ratio', 0):.2%}")

    with st.expander("Employment & Stability"):
        c1, c2 = st.columns(2)
        c1.metric("Occupation", profile.get('emp_occupation', 'N/A'))
        c2.metric("Employer Type", profile.get('emp_employer_type', 'N/A'))
        st.metric("Tenure (Years)", profile.get('emp_tenure_years', 0))

    with st.expander("Behavioral & External Credit"):
        c1, c2, c3 = st.columns(3)
        c1.metric("CIBIL Score", profile.get('ext_cibil_score', 0))
        c2.metric("EMI Bounces", profile.get('beh_past_emi_bounces', 0))
        c3.metric("Credit Utilization", f"{profile.get('beh_avg_credit_utilization', 0):.1%}")

# --- Main Router ---
if st.session_state.page == 'input':
    render_input_screen()
else:
    render_report_screen()
