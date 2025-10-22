# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")
st.title("🛍️ E-Commerce Analytics Dashboard")


@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_data.csv", parse_dates=['InvoiceDate'], low_memory=False)
    df['month'] = df['InvoiceDate'].dt.to_period('M').astype(str)
    df['revenue'] = df['Quantity'] * df['UnitPrice']
    return df


df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
country = st.sidebar.selectbox("Country", ["All"] + sorted(df['Country'].dropna().unique().tolist()))
month = st.sidebar.selectbox("Month", ["All"] + sorted(df['month'].unique().tolist()))

# Filter dataframe
df_filtered = df.copy()
if country != "All":
    df_filtered = df_filtered[df_filtered['Country'] == Country]
if month != "All":
    df_filtered = df_filtered[df_filtered['month'] == month]

# KPI cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${df_filtered['revenue'].sum():,.0f}")
col2.metric("Unique Customers", f"{df_filtered['CustomerID'].nunique()}")
col3.metric("Avg Order Value", f"${df_filtered.groupby('InvoiceNo')['revenue'].sum().mean():.2f}")
col4.metric("Repeat Rate", f"{(df_filtered.groupby('CustomerID')['InvoiceNo'].nunique() > 1).mean():.2%}")

# Monthly revenue chart
st.subheader("Monthly Revenue")
monthly = df_filtered.groupby('month')['revenue'].sum().reset_index()
fig = px.line(monthly, x='month', y='revenue', markers=True)
st.plotly_chart(fig, use_container_width=True)

# Top products
st.subheader("Top Products by Quantity")
top_products = df_filtered.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10).reset_index()
fig2 = px.bar(top_products, x='Description', y='Quantity')
fig2.update_xaxes(tickangle=45)
st.plotly_chart(fig2, use_container_width=True)

# Customer table (sample)
st.subheader("Sample Customers")
st.dataframe(df_filtered.groupby('customerid').agg({'revenue':'sum','invoiceno':'nunique'}).reset_index().sort_values('revenue', ascending=False).head(10))




