import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=['Order_Date'])

# Title and introduction
st.title("Data App Assignment - Sales Dashboard")

# Dropdown for Category selection
category = st.selectbox("Select a Category", df["Category"].unique())

# Multi-select for Sub_Category based on selected Category
sub_categories = st.multiselect("Select Sub_Categories", 
                                df[df["Category"] == category]["Sub_Category"].unique())

# Filter the data based on the selected Category and Sub_Categories
filtered_data = df[(df["Category"] == category) & (df["Sub_Category"].isin(sub_categories))]

# Line chart of sales for the selected items
if not filtered_data.empty:
    sales_by_date = filtered_data.groupby("Order_Date").sum()["Sales"]
    st.line_chart(sales_by_date, use_container_width=True)

    # Calculate metrics for the selected items
    total_sales = filtered_data["Sales"].sum()
    total_profit = filtered_data["Profit"].sum()
    profit_margin = total_profit / total_sales if total_sales != 0 else 0
    
    # Calculate the overall average profit margin for all data
    overall_total_sales = df["Sales"].sum()
    overall_total_profit = df["Profit"].sum()
    overall_profit_margin = overall_total_profit / overall_total_sales if overall_total_sales != 0 else 0

    # Delta for profit margin
    delta_profit_margin = profit_margin - overall_profit_margin

    # Display metrics
    st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
    st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
    st.metric(label="Profit Margin", value=f"{profit_margin:.2%}", delta=f"{delta_profit_margin:.2%}")
else:
    st.write("Please select Sub-Categories to view data.")


