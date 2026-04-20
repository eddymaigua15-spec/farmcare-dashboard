import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("Surgeons FarmCare Sales Dashboard")

# Sample dataset (you can replace later)
data = {
    "Product": ["Maclik Super", "Nilzan", "Kupakula", "Triatix"],
    "Region": ["Embu", "Meru", "Embu", "Kirinyaga"],
    "Sales": [120, 90, 150, 70]
}

df = pd.DataFrame(data)

# Sidebar filter
st.sidebar.header("Filter Options")
region = st.sidebar.selectbox("Select Region", df["Region"].unique())

# Filter data
filtered_df = df[df["Region"] == region]

# Show data
st.subheader(f"Sales Data for {region}")
st.write(filtered_df)

# Chart
st.subheader("Sales Performance")
fig, ax = plt.subplots()
ax.bar(filtered_df["Product"], filtered_df["Sales"])
st.pyplot(fig)

# KPI
total_sales = filtered_df["Sales"].sum()
st.metric("Total Sales", total_sales)