import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("attrition_predictions.csv")

st.set_page_config(page_title="Attrition BI Dashboard", layout="wide")
st.title(" Employee Attrition Prediction Dashboard")

# KPIs
attrition_rate = df['Attrition_Prediction'].mean() * 100
avg_income = df['MonthlyIncome'].mean()
high_risk_count = (df['Attrition_Prob'] > 0.7).sum()

col1, col2, col3 = st.columns(3)
col1.metric("Attrition Rate", f"{attrition_rate:.2f}%")
col2.metric("Avg. Monthly Income", f"₹{avg_income:,.0f}")
col3.metric("High Risk Employees", high_risk_count)

# Filters
Age = st.sidebar.selectbox("Select Age", ['All'] + sorted(df['Age'].unique()))
if Age != 'All':
    df = df[df['Age'] == Age]

# Plots

fig = px.scatter(df, x='MonthlyIncome', y='JobSatisfaction',
                  color='Attrition_Prediction',
                  title="Income vs Satisfaction vs Attrition")
st.plotly_chart(fig, use_container_width=True)

# Table of high-risk employees
# Table of high-risk employees with more metrics
st.subheader(" High Risk Employee Table (Attrition Prob > 0.7)")

# List of columns to show (filtered based on actual dataset)
columns_to_show = [
    'Age', 'Attrition_Prob', 'JobSatisfaction', 'MonthlyIncome',
    'YearsAtCompany', 'WorkLifeBalance', 'PerformanceRating',
    'DistanceFromHome', 'EnvironmentSatisfaction'
]

# Filter and display table
high_risk_df = df[df['Attrition_Prob'] > 0.7][columns_to_show].sort_values(
    by='Attrition_Prob', ascending=False
)

st.dataframe(high_risk_df)
