import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from datetime import datetime, timedelta

# Page Configuration
st.set_page_config(
    page_title="Coffee Shop Sales Analysis",
    page_icon="☕",
    layout="wide"
)

# Helper function to generate data
@st.cache_data
def generate_data(num_records=1000):
    # Define products and prices
    menu = {
        'Coffee': {'Espresso': 2.50, 'Latte': 4.00, 'Cappuccino': 3.75, 'Americano': 3.00, 'Mocha': 4.50},
        'Tea': {'Green Tea': 2.75, 'Black Tea': 2.50, 'Herbal Tea': 3.00, 'Chai Latte': 4.25},
        'Bakery': {'Croissant': 3.50, 'Muffin': 2.75, 'Scone': 3.00, 'Bagel': 2.50},
        'Sandwich': {'Ham & Cheese': 6.50, 'Veggie Wrap': 7.00, 'Turkey Club': 7.50}
    }
    
    products = []
    categories = []
    prices = []
    
    for cat, items in menu.items():
        for item, price in items.items():
            products.append(item)
            categories.append(cat)
            prices.append(price)
            
    # Time range: Last 6 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    data = []
    
    for i in range(num_records):
        date = start_date + timedelta(days=random.randint(0, 180))
        
        # Determine hour: peaks around 8-10am and 12-2pm
        hour_prob = [0.01]*7 + [0.15, 0.20, 0.15, 0.10, 0.15, 0.10, 0.05, 0.05, 0.02, 0.01, 0.01] + [0]*6
        hour_prob = np.array(hour_prob)
        hour_prob /= hour_prob.sum() 
        hour = np.random.choice(range(24), p=hour_prob)
        minute = random.randint(0, 59)
        order_time = date.replace(hour=hour, minute=minute, second=0)
        
        idx = random.randint(0, len(products)-1)
        item = products[idx]
        category = categories[idx]
        base_price = prices[idx]
        
        qty = np.random.choice([1, 2, 3], p=[0.8, 0.15, 0.05])
        total_price = base_price * qty
        
        payment_methods = ['Card', 'Cash', 'Mobile Payment']
        payment = np.random.choice(payment_methods, p=[0.6, 0.25, 0.15])
        
        rating = np.random.choice([1, 2, 3, 4, 5], p=[0.02, 0.03, 0.10, 0.35, 0.50])
        
        data.append([i+1, order_time.date(), order_time.time(), item, category, qty, base_price, total_price, payment, rating])
        
    df = pd.DataFrame(data, columns=['Order ID', 'Date', 'Time', 'Item', 'Category', 'Quantity', 'Unit Price', 'Total Sales', 'Payment Method', 'Rating'])
    df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str))
    
    return df

# Main App Layout
st.title("☕ Coffee Shop Business Analysis")
st.markdown("Deep dive into sales trends, product performance, and customer behavior.")

# Sidebar
st.sidebar.header("Data Settings")
num_records = st.sidebar.slider("Number of Transactions", 500, 5000, 1000)

if st.sidebar.button("Generate New Data"):
    st.cache_data.clear()
    df = generate_data(num_records)
    st.sidebar.success(f"Generated {num_records} new records!")
else:
    # Try to load existing or generate default
    try:
        df = generate_data(num_records)
    except:
        df = generate_data(1000)

# 1. KPI Metrics
st.header("Key Performance Indicators (KPIs)")
col1, col2, col3, col4 = st.columns(4)

total_revenue = df['Total Sales'].sum()
total_orders = len(df)
avg_order_value = df['Total Sales'].mean()
avg_rating = df['Rating'].mean()

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders}")
col3.metric("Avg Order Value", f"${avg_order_value:.2f}")
col4.metric("Avg Customer Rating", f"{avg_rating:.1f} ⭐")

st.divider()

# Tabs for detailed analysis
tab1, tab2, tab3 = st.tabs(["📊 Charts & Analysis", "📈 Statistical Insights", "📄 Raw Data"])

with tab1:
    st.subheader("Visual Sales Analysis")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("**Sales Trend over Time**")
        df['Month'] = df['Datetime'].dt.to_period('M').astype(str)
        monthly_sales = df.groupby('Month')['Total Sales'].sum().reset_index()
        
        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.barplot(data=monthly_sales, x='Month', y='Total Sales', color='skyblue', ax=ax1)
        ax1.set_xlabel('Month')
        ax1.set_ylabel('Total Sales ($)')
        plt.xticks(rotation=45)
        st.pyplot(fig1)

    with col_chart2:
        st.markdown("**Sales Distribution by Category**")
        cat_sales = df.groupby('Category')['Total Sales'].sum()
        
        fig2, ax2 = plt.subplots(figsize=(8, 8))
        ax2.pie(cat_sales, labels=cat_sales.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
        st.pyplot(fig2)

    st.markdown("---")
    
    col_chart3, col_chart4 = st.columns(2)
    
    with col_chart3:
        st.markdown("**Top 8 Best Selling Items**")
        top_items = df.groupby('Item')['Quantity'].sum().sort_values(ascending=False).head(8)
        
        fig3, ax3 = plt.subplots(figsize=(10, 6))
        sns.barplot(x=top_items.values, y=top_items.index, palette="viridis", ax=ax3)
        ax3.set_xlabel('Quantity Sold')
        st.pyplot(fig3)

    with col_chart4:
        st.markdown("**Peak Hours Heatmap**")
        df['Hour'] = df['Datetime'].dt.hour
        df['DayOfWeek'] = df['Datetime'].dt.day_name()
        
        pivot_table = df.pivot_table(index='DayOfWeek', columns='Hour', values='Order ID', aggfunc='count')
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot_table = pivot_table.reindex(days_order)
        
        fig4, ax4 = plt.subplots(figsize=(12, 6))
        sns.heatmap(pivot_table, cmap="YlOrRd", linewidths=.5, ax=ax4)
        st.pyplot(fig4)

with tab2:
    st.subheader("Statistical Deep Dive")
    
    col_stat1, col_stat2 = st.columns(2)
    
    with col_stat1:
        st.markdown("#### Sales by Category")
        st.dataframe(df.groupby('Category')['Total Sales'].sum().sort_values(ascending=False))
        
        st.markdown("#### Payment Method Distribution")
        st.dataframe(df['Payment Method'].value_counts(normalize=True).mul(100).round(2).astype(str) + '%')

    with col_stat2:
        st.markdown("#### Top 5 Items by Quantity")
        st.dataframe(df.groupby('Item')['Quantity'].sum().sort_values(ascending=False).head(5))
        
        peak_hour = df.groupby('Hour')['Order ID'].count().idxmax()
        st.info(f"💡 The store's busiest time is around **{peak_hour}:00**.")

with tab3:
    st.subheader("Raw Transaction Data")
    st.dataframe(df)

