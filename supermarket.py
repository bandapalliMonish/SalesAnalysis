# %%
import pandas as pd


# %%
sales_df = pd.read_csv("Data Science Internship Assignment Datasets/sales.csv")
promotion_df = pd.read_csv("Data Science Internship Assignment Datasets/promotion.csv")
items_df = pd.read_csv("Data Science Internship Assignment Datasets/item.csv")
supermarkets_df = pd.read_csv("Data Science Internship Assignment Datasets/supermarkets.csv")


# %%
print(sales_df.info())
print(sales_df.head())

print(promotion_df.info())
print(promotion_df.head())

print(items_df.info())
print(items_df.head())

print(supermarkets_df.info())
print(supermarkets_df.head())


# %%
print(sales_df.isnull().sum())
print(promotion_df.isnull().sum())
print(items_df.isnull().sum())
print(supermarkets_df.isnull().sum())


# %%
print(sales_df.duplicated().sum())
print(promotion_df.duplicated().sum())
print(items_df.duplicated().sum())
print(supermarkets_df.duplicated().sum())


# %%
# For instance, check for missing values and handle them (drop or fill with appropriate values)
items_df = items_df.dropna()  # or use items_df.fillna('Unknown') based on the data
sales_df = sales_df.dropna(subset=['amount', 'units', 'code'])  # Drop rows where critical fields are missing
promotion_df = promotion_df.dropna(subset=['code', 'supermarkets'])  # Drop rows where critical fields are missing
supermarkets_df = supermarkets_df.dropna(subset=['supermarket_No'])

# %%
items_df.columns = items_df.columns.str.strip().str.lower()  # Clean column names
sales_df.columns = sales_df.columns.str.strip().str.lower()
promotion_df.columns = promotion_df.columns.str.strip().str.lower()
supermarkets_df.columns = supermarkets_df.columns.str.strip().str.lower()

# %%
# Step 4: Standardize column names for consistency
for df in [items_df, sales_df, promotion_df, supermarkets_df]:
    df.columns = df.columns.str.strip().str.lower().str.replace('_', '')

# Match similar column names across all dataframes
column_mapping = {
    'supermarketno': 'supermarket',
    'supermarkets': 'supermarket',
    'descrption': 'description'
}
for df in [items_df, sales_df, promotion_df, supermarkets_df]:
    df.rename(columns=column_mapping, inplace=True)

# %%
for df in [items_df, sales_df, promotion_df, supermarkets_df]:
    print(df.columns)

# %%
print(sales_df['time'])

# %%
# Ensure all time values are 4 digits (e.g., '8' becomes '0800')
sales_df['time'] = sales_df['time'].astype(str).str.zfill(4)

# Convert the time column to HH:MM format
sales_df['time'] = pd.to_datetime(sales_df['time'], format='%H%M').dt.strftime('%H:%M')

# Convert 'week' in promotion to numeric if needed
promotion_df['week'] = pd.to_numeric(promotion_df['week'], errors='coerce')

# Convert 'amount' and 'units' in sales to numeric
sales_df['amount'] = pd.to_numeric(sales_df['amount'], errors='coerce')
sales_df['units'] = pd.to_numeric(sales_df['units'], errors='coerce')

# %%
# Merging sales data with item data based on 'code'
sales_items_df = pd.merge(sales_df, items_df, on='code', how='left')

print(sales_items_df.columns)


# %%
# Merging sales data with promotions
sales_promotion_df = pd.merge(sales_items_df, promotion_df, on=['code', 'supermarket'], how='left')
print(sales_promotion_df.columns)

# %%

# Merging with supermarket info
final_df = pd.merge(sales_promotion_df, supermarkets_df, on='supermarket', how='left')


# %%
# For example, create a new column for sales revenue (amount * units)
final_df['revenue'] = final_df['amount'] * final_df['units']

# Step 8: Save cleaned and transformed data to a new CSV or DataFrame
final_df.to_csv('cleaned_sales_data.csv', index=False)

print("Data cleaning and transformation complete.")
