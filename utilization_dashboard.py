import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Utilization Dashboard")

# --- Load Data ---
uploaded_file = st.file_uploader("Upload Utilization Log CSV", type="csv", key="fileuploader")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    df["Date"] = pd.to_datetime(df["Date"])

    # --- KPI Row ---
    total_hours = df["Hours Spent"].sum()
    unique_trainees = df["Trainee Name"].nunique()
    avg_hours_per_trainee = df.groupby("Trainee Name")["Hours Spent"].sum().mean().round(2)
    total_days = df["Date"].nunique()

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Total Hours", f"{total_hours}")
    kpi2.metric("Unique Trainees", f"{unique_trainees}")
    kpi3.metric("Avg Hours/Trainee", f"{avg_hours_per_trainee}")
    kpi4.metric("Total Days Logged", f"{total_days}")

    st.markdown("---")

    # --- Category Bar Chart ---
    cat_hours = df.groupby("Category")["Hours Spent"].sum().sort_values()
    st.subheader("Category Breakdown")
    st.bar_chart(cat_hours)

    # --- Pie Chart for Category Distribution ---
    fig1, ax1 = plt.subplots()
    ax1.pie(cat_hours, labels=cat_hours.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)

    # --- Line Chart: Utilization Over Time ---
    st.subheader("Utilization Over Time")
    time_series = df.groupby("Date")["Hours Spent"].sum()
    st.line_chart(time_series)

    # --- Data Table ---
    st.subheader("Detailed Log")
    st.dataframe(df)
else:
    st.info("Please upload your academy_ph_utilization_log.csv file to begin.")