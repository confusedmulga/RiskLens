import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="RiskLens Dashboard", layout="wide")
st.title("RiskLens: Credit Risk Analytics Dashboard")

# Sidebar
st.sidebar.header("Filters")
st.sidebar.selectbox("Portfolio Segment", ["All", "High Risk", "Medium Risk", "Low Risk"])
st.sidebar.slider("Risk Score Threshold", 0.0, 1.0, 0.7, 0.01)

# Main heatmap (placeholder)
st.subheader("Portfolio Heatmap by Risk Segment")
data = np.random.rand(10, 10)
fig, ax = plt.subplots()
cax = ax.matshow(data, cmap='coolwarm')
fig.colorbar(cax)
st.pyplot(fig)

# Per-borrower risk radar (placeholder)
st.subheader("Per-Borrower 'Risk Radar' Chart")
labels = ["DPD", "Utilization", "Velocity", "Proxies", "Product Mix"]
values = list(np.random.rand(len(labels)))
values.append(values[0])  # close the loop
angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True)

fig2, ax2 = plt.subplots(subplot_kw={"polar": True})
ax2.plot(angles, values, "o-", linewidth=2)
ax2.fill(angles, values, alpha=0.25)
ax2.set_xticks(angles[:-1])
ax2.set_xticklabels(labels)
ax2.set_title("Sample Borrower Risk Profile")
st.pyplot(fig2)

# Time-slider (placeholder)
st.subheader("Time Slider: Replay Risk Evolution")
time = st.slider("Select Time Point", 0, 12, 0)
st.write(f"Showing data for month: {time}")

st.info("This is a demo dashboard. Connect real data and models to power the visualizations.")