import pandas as pd
import matplotlib.pyplot as plt


# 1. Load Dataset

df = pd.read_csv(r"C:\Users\dhans\Downloads\sales_data.csv")

# 2. Clean Column Names

df.columns = df.columns.str.strip().str.lower()
print("Columns found:", df.columns.tolist())

# 3. Detect Required Columns

date_col = None
product_col = None
sales_col = None

for col in df.columns:
    if "date" in col:
        date_col = col
    elif "product" in col or "item" in col or "category" in col:
        product_col = col
    elif "amount" in col or "sales" in col or "price" in col:
        sales_col = col

if not date_col or not product_col or not sales_col:
    print("Required columns not found. Check dataset.")
    exit()

# 4. Data Cleaning

df = df[[date_col, product_col, sales_col]]
df.dropna(inplace=True)

df[date_col] = pd.to_datetime(df[date_col])
df[sales_col] = df[sales_col].astype(float)

# 5. Sales Analysis

total_sales = df[sales_col].sum()

product_sales = (
    df.groupby(product_col)[sales_col]
    .sum()
    .sort_values(ascending=False)
)

monthly_sales = (
    df.groupby(df[date_col].dt.month)[sales_col]
    .sum()
)

print("\n----- E-COMMERCE SALES SUMMARY -----")
print("Total Sales:", total_sales)
print("\nTop Selling Products:")
print(product_sales.head())

# 6. Visualization 1: Bar Chart

plt.figure()
product_sales.head(10).plot(kind="bar")
plt.title("Top 10 Best-Selling Products")
plt.xlabel("Product")
plt.ylabel("Sales Amount")
plt.tight_layout()
plt.show()

# 7. Visualization 2: Line Chart

plt.figure()
monthly_sales.plot(kind="line", marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales Amount")
plt.tight_layout()
plt.show()

# 8. Insights

best_product = product_sales.idxmax()
best_sales = product_sales.max()

print("\n----- INSIGHTS -----")
print(f"Best-selling product: {best_product}")
print(f"Revenue from best product: {best_sales}")
print("Sales peak months can be targeted for promotions.")
