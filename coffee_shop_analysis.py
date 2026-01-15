import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
from datetime import datetime, timedelta

# Set random seed for reproducibility
np.random.seed(42)

def generate_data(num_records=1000):
    print("Generating synthetic data...")
    
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
        # Random date and time (weighted towards morning/lunch)
        date = start_date + timedelta(days=random.randint(0, 180))
        
        # Determine hour: peaks around 8-10am and 12-2pm
        hour_prob = [0.01]*7 + [0.15, 0.20, 0.15, 0.10, 0.15, 0.10, 0.05, 0.05, 0.02, 0.01, 0.01] + [0]*6
        hour_prob = np.array(hour_prob)
        hour_prob /= hour_prob.sum() # Normalize to sum to 1
        hour = np.random.choice(range(24), p=hour_prob)
        minute = random.randint(0, 59)
        order_time = date.replace(hour=hour, minute=minute, second=0)
        
        # Select product
        idx = random.randint(0, len(products)-1)
        item = products[idx]
        category = categories[idx]
        base_price = prices[idx]
        
        # Quantity (mostly 1, sometimes 2 or 3)
        qty = np.random.choice([1, 2, 3], p=[0.8, 0.15, 0.05])
        
        total_price = base_price * qty
        
        payment_methods = ['Card', 'Cash', 'Mobile Payment']
        payment = np.random.choice(payment_methods, p=[0.6, 0.25, 0.15])
        
        rating = np.random.choice([1, 2, 3, 4, 5], p=[0.02, 0.03, 0.10, 0.35, 0.50])
        
        data.append([i+1, order_time.date(), order_time.time(), item, category, qty, base_price, total_price, payment, rating])
        
    df = pd.DataFrame(data, columns=['Order ID', 'Date', 'Time', 'Item', 'Category', 'Quantity', 'Unit Price', 'Total Sales', 'Payment Method', 'Rating'])
    
    # Add datetime column for easier analysis
    df['Datetime'] = pd.to_datetime(df['Date'].astype(str) + ' ' + df['Time'].astype(str))
    
    filename = 'coffee_shop_sales.csv'
    df.to_csv(filename, index=False)
    print(f"Data generated and saved to {filename}")
    return df

def analyze_data(df):
    print("\n--- Deep Data Analysis ---")
    
    # 1. Basic Stats
    print("\n1. General Overview:")
    print(df.describe())
    print(f"\nTotal Revenue: ${df['Total Sales'].sum():.2f}")
    print(f"Total Orders: {len(df)}")
    print(f"Average Transaction Value: ${df['Total Sales'].mean():.2f}")
    
    # 2. Sales by Category
    print("\n2. Sales by Category:")
    cat_sales = df.groupby('Category')['Total Sales'].sum().sort_values(ascending=False)
    print(cat_sales)
    
    # 3. Top Selling Items
    print("\n3. Top 5 Best Selling Items:")
    item_sales = df.groupby('Item')['Quantity'].sum().sort_values(ascending=False).head(5)
    print(item_sales)
    
    # 4. Hourly Trends
    df['Hour'] = df['Datetime'].dt.hour
    hourly_counts = df.groupby('Hour')['Order ID'].count()
    peak_hour = hourly_counts.idxmax()
    print(f"\n4. Peak Hour: {peak_hour}:00")

    # 5. Payment Methods
    print("\n5. Payment Method Distribution:")
    print(df['Payment Method'].value_counts(normalize=True) * 100)

    return df

def visualize_data(df):
    print("\nGenerating Visualizations...")
    sns.set_theme(style="whitegrid")
    
    # 1. Sales Trend over Time (Monthly)
    df['Month'] = df['Datetime'].dt.to_period('M')
    monthly_sales = df.groupby('Month')['Total Sales'].sum()
    
    plt.figure(figsize=(10, 6))
    monthly_sales.plot(kind='bar', color='skyblue')
    plt.title('Monthly Sales Trend')
    plt.xlabel('Month')
    plt.ylabel('Total Sales ($)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('sales_trend.png')
    plt.close()
    
    # 2. Category Distribution (Pie Chart)
    cat_sales = df.groupby('Category')['Total Sales'].sum()
    plt.figure(figsize=(8, 8))
    plt.pie(cat_sales, labels=cat_sales.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("pastel"))
    plt.title('Sales Distribution by Category')
    plt.tight_layout()
    plt.savefig('category_distribution.png')
    plt.close()
    
    # 3. Top Items (Bar Chart)
    top_items = df.groupby('Item')['Quantity'].sum().sort_values(ascending=False).head(8)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_items.values, y=top_items.index, palette="viridis")
    plt.title('Top 8 Best Selling Items (Quantity)')
    plt.xlabel('Quantity Sold')
    plt.tight_layout()
    plt.savefig('top_items.png')
    plt.close()
    
    # 4. Hourly Heatmap (Day of Week vs Hour)
    df['DayOfWeek'] = df['Datetime'].dt.day_name()
    pivot_table = df.pivot_table(index='DayOfWeek', columns='Hour', values='Order ID', aggfunc='count')
    # Reorder days
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_table = pivot_table.reindex(days_order)
    
    plt.figure(figsize=(12, 6))
    sns.heatmap(pivot_table, cmap="YlOrRd", linewidths=.5)
    plt.title('Heatmap of Orders: Day vs Hour')
    plt.tight_layout()
    plt.savefig('hourly_heatmap.png')
    plt.close()
    
    print("Visualizations saved: sales_trend.png, category_distribution.png, top_items.png, hourly_heatmap.png")

if __name__ == "__main__":
    df = generate_data(1000)
    analyze_data(df)
    visualize_data(df)
