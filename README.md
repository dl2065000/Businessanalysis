# Coffee Shop Business Data Analysis

This project generates a synthetic dataset for a small coffee shop and performs deep exploratory data analysis (EDA) using Python. It includes automated data generation, statistical analysis, and data visualization to provide business insights.

## Project Structure

- `coffee_shop_analysis.py`: The main Python script that generates the data, performs analysis, and creates visualizations.
- `coffee_shop_sales.csv`: The generated synthetic dataset containing 1,000 transaction records.
- `*.png`: Visualizations generated during the analysis:
  - `sales_trend.png`: Monthly revenue trends.
  - `category_distribution.png`: Sales breakdown by category (Coffee, Tea, Bakery, Sandwich).
  - `top_items.png`: Most popular items by quantity sold.
  - `hourly_heatmap.png`: Heatmap showing peak business hours across the week.

## Dataset Features

The synthetic dataset includes the following fields:
- **Order ID**: Unique identifier for each transaction.
- **Date & Time**: When the order occurred.
- **Item**: The specific product purchased (e.g., Espresso, Latte, Veggie Wrap).
- **Category**: Product group (Coffee, Tea, Bakery, Sandwich).
- **Quantity**: Number of items in the order.
- **Unit Price**: Price per item.
- **Total Sales**: Total amount for the transaction.
- **Payment Method**: Card, Cash, or Mobile Payment.
- **Rating**: Customer satisfaction score (1-5).

## Installation & Usage

### Prerequisites
- Python 3.x
- Required libraries: `pandas`, `numpy`, `matplotlib`, `seaborn`

### Setup
Install the dependencies using pip:
```bash
python -m pip install pandas numpy matplotlib seaborn
```

### Running the Analysis
Execute the script to regenerate the dataset and update the analysis:
```bash
python coffee_shop_analysis.py
```

## Business Insights from Analysis

1. **Peak Hours**: The analysis identifies peak morning hours (8:00 AM - 10:00 AM), helping with staff scheduling.
2. **Product Performance**: Identifies top revenue-generating categories and best-selling individual items.
3. **Payment Preferences**: Analyzes how customers prefer to pay, which can inform POS system choices.
4. **Customer Satisfaction**: Tracks average ratings to monitor service quality.

## License
This project is open-source and intended for educational purposes.
