import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Data App Assignment, on Oct 7th")

st.write("### Input Data and Examples")
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=True)
st.dataframe(df)

# Add a dropdown for selecting a specific category
categories = df['Category'].unique()  # Get unique categories from the data
selected_category = st.selectbox("Select a Category", categories)

# Filter data based on the selected category
filtered_df = df[df['Category'] == selected_category]

# Add a multi-select for Sub-Category within the selected Category
sub_categories = filtered_df['Sub-Category'].unique()
selected_sub_categories = st.multiselect("Select Sub-Categories", sub_categories, default=sub_categories)

# Filter data based on the selected sub-categories
filtered_sub_df = filtered_df[filtered_df['Sub-Category'].isin(selected_sub_categories)]

# Line chart of sales for the selected sub-categories
st.write(f"### Sales Data for {selected_category} - Selected Sub-Categories")
sales_by_date = filtered_sub_df.groupby('Order_Date')['Sales'].sum()
st.line_chart(sales_by_date)

# Calculate total sales, total profit, and profit margin for the selected sub-categories
total_sales = filtered_sub_df['Sales'].sum()
total_profit = filtered_sub_df['Profit'].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

# Calculate overall profit margin across all categories for comparison
overall_total_sales = df['Sales'].sum()
overall_total_profit = df['Profit'].sum()
overall_profit_margin = (overall_total_profit / overall_total_sales) * 100 if overall_total_sales > 0 else 0

# Show metrics with delta for profit margin
st.write("### Metrics for Selected Sub-Categories")
st.metric("Total Sales", f"${total_sales:,.2f}")
st.metric("Total Profit", f"${total_profit:,.2f}")
st.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%",
    delta=f"{profit_margin - overall_profit_margin:.2f}%",
    delta_color="normal"
)

# Aggregating Sales by Category for overall comparison
st.write("### Aggregated Sales by Category")
aggregated_sales = df.groupby("Category", as_index=False).sum()

# Show aggregated data
st.dataframe(aggregated_sales)

# Bar chart of aggregated sales by category
st.bar_chart(aggregated_sales, x="Category", y="Sales", color="#04f")

# Aggregating by time
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df.set_index('Order_Date', inplace=True)
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.write("### Aggregated Sales by Month")
st.line_chart(sales_by_month)

