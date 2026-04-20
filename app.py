import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ========================================
# PAGE CONFIG
# ========================================
st.set_page_config(page_title="FarmCare Intelligence", layout="wide")
st.title("Surgeons FarmCare | Territory Intelligence System")
st.write("Upload your sales file or use default dataset")

# ========================================
# DATA INPUT LAYER
# ========================================
uploaded_file = st.file_uploader("Upload Sales CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    # Default dataset (fallback)
    df = pd.DataFrame({
        "Product": ["Maclik Super", "Nilzan", "Kupakula", "Triatix", "Maclik Super", "Nilzan"],
        "Region": ["Embu", "Embu", "Meru", "Kirinyaga", "Meru", "Embu"],
        "Sales": [120, 90, 150, 70, 110, 95],
        "Profit": [30, 20, 45, 18, 28, 22],
        "Month": ["Jan", "Jan", "Feb", "Feb", "Mar", "Jan"]
    })

# ========================================
# FILTERS (CONTROL PANEL)
# ========================================
st.sidebar.header("Control Panel")
region = st.sidebar.selectbox("Select Region", df["Region"].unique())
product = st.sidebar.selectbox("Select Product", df["Product"].unique())

filtered_df = df[(df["Region"] == region) & (df["Product"] == product)]

# ========================================
# KPI ENGINE
# ========================================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Sales", filtered_df["Sales"].sum())

with col2:
    st.metric("Total Profit", filtered_df["Profit"].sum())

with col3:
    avg_sales = round(filtered_df["Sales"].mean(), 2) if len(filtered_df) > 0 else 0
    st.metric("Avg Sales per Transaction", avg_sales)

# ========================================
# DATA VIEW
# ========================================
st.subheader("Filtered Sales Dataset")
st.dataframe(filtered_df)

# ========================================
# VISUALIZATIONS
# ========================================
st.subheader("Sales Distribution by Product")
fig1, ax1 = plt.subplots(figsize=(10, 5))
region_data = df[df["Region"] == region].groupby("Product")["Sales"].sum()
ax1.bar(region_data.index, region_data.values, color="steelblue")
ax1.set_ylabel("Sales Volume")
ax1.set_xlabel("Products")
ax1.set_title(f"Sales by Product - {region}")
st.pyplot(fig1)

# Sales trend by month (if data exists)
if "Month" in df.columns:
    st.subheader("Sales Trend by Month")
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    trend = df[df["Product"] == product].groupby("Month")["Sales"].sum()
    ax2.plot(trend.index, trend.values, marker="o", linewidth=2, markersize=8, color="darkgreen")
    ax2.set_ylabel("Sales")
    ax2.set_xlabel("Month")
    ax2.set_title(f"Sales Trend - {product}")
    ax2.grid(True, alpha=0.3)
    st.pyplot(fig2)

# ========================================
# BUSINESS INSIGHT ENGINE
# ========================================
st.subheader("Key Insight")
total_sales = filtered_df["Sales"].sum()

if total_sales > 100:
    st.success("✅ High performing product in selected segment")
else:
    st.warning("⚠️ Low sales performance detected — review distribution or pricing strategy")

st.info(f"📊 Current Selection: {product} in {region} | Total Sales: {total_sales}")
