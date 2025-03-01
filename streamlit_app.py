import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=['Order_Date'])

# Title and data display
st.title("Data App Use Cases")
st.write("### Sales Analysis by Category and Sub-Category")
st.dataframe(df)

# Dropdown for Category selection
selected_category = st.selectbox("Select a Category", df['Category'].unique())

# Multi-select for Sub-Category based on the selected Category
filtered_df = df[df['Category'] == selected_category]
selected_subcategories = st.multiselect("Select Sub_Category", filtered_df['Sub_Category'].unique())

# Filter the dataframe by selected sub-categories
filtered_df = filtered_df[filtered_df['Sub_Category'].isin(selected_subcategories)]

# Sort by Order_Date to ensure the line chart is in ascending order by date
filtered_df = filtered_df.sort_values(by='Order_Date')

# Create a line chart for Sales with different colors for each Sub-Category
plt.figure(figsize=(10, 6))
for subcategory in selected_subcategories:
    subcategory_data = filtered_df[filtered_df['Sub_Category'] == subcategory]
    plt.plot(subcategory_data['Order_Date'], subcategory_data['Sales'], label=subcategory)

plt.title('Sales by Sub-Category')
plt.xlabel('Order Date')
plt.ylabel('Sales')
plt.legend(title='Sub-Category')
plt.xticks(rotation=45)
plt.tight_layout()

# Show the plot in Streamlit
st.pyplot(plt)

# Calculate metrics for selected items
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

# Calculate overall average profit margin
overall_total_sales = df['Sales'].sum()
overall_total_profit = df['Profit'].sum()
overall_profit_margin = (overall_total_profit / overall_total_sales) * 100 if overall_total_sales > 0 else 0

# Display metrics with delta for profit margin
st.metric(label="Total Sales", value=f"${total_sales:,.2f}")
st.metric(label="Total Profit", value=f"${total_profit:,.2f}")
st.metric(label="Profit Margin", value=f"{profit_margin:.2f}%", delta=f"{profit_margin - overall_profit_margin:.2f}%")



