import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)

# Streamlit app title
st.title("Sales Dashboard")

# Category dropdown
category = st.selectbox('Select a Category', df['Category'].unique())

# Filter sub-categories based on selected category
filtered_df = df[df['Category'] == category]
sub_categories = st.multiselect('Select Sub_Category', filtered_df['Sub_Category'].unique())

# Further filter based on selected sub-categories
if sub_categories:
    filtered_df = filtered_df[filtered_df['Sub_Category'].isin(sub_categories)]

# Show a line chart of sales for selected items
if not filtered_df.empty:
    # Group sales by Order Date for selected Sub-Categories
    sales_by_date = filtered_df.groupby('Order_Date').sum()['Sales']
    st.line_chart(sales_by_date)

# Calculate metrics for selected items
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

# Calculate overall average profit margin
overall_total_sales = df['Sales'].sum()
overall_total_profit = df['Profit'].sum()
overall_profit_margin = (overall_total_profit / overall_total_sales) * 100 if overall_total_sales > 0 else 0

# Display metrics
st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
st.metric(label="Profit Margin", value=f"{profit_margin:.2f}%", delta=f"{profit_margin - overall_profit_margin:.2f}%")

# Display data frame of the filtered results
st.dataframe(filtered_df)



