import pandas as pd

# Load file
df = pd.read_csv("C:/Users/Dell/Desktop/Datasets/Brazilian E-Commerce Public Dataset by Olist/olist_order_items_dataset.csv")

print("=== BASIC OVERVIEW ===")
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\n=== NULL CHECK ===")
print(df.isna().sum())

print("\n=== EXACT DUPLICATES ===")
print("Duplicate rows:", df.duplicated().sum())

print("\n=== BUSINESS KEY UNIQUENESS CHECK ===")
dup_key = df.duplicated(subset=["order_id", "order_item_id"]).sum()
print("Duplicate (order_id, order_item_id):", dup_key)

print("\n=== TEXT ID QUALITY CHECK ===")
id_cols = ["order_id", "product_id", "seller_id"]
for col in id_cols:
    spaces = (df[col].astype(str) != df[col].astype(str).str.strip()).sum()
    blanks = df[col].astype(str).str.strip().eq("").sum()
    print(f"{col} -> spaces: {spaces}, blanks: {blanks}")

print("\n=== DATE VALIDITY CHECK ===")
parsed_dates = pd.to_datetime(df["shipping_limit_date"], errors="coerce")
invalid_dates = parsed_dates.isna().sum()
print("Invalid shipping_limit_date:", invalid_dates)

print("\nDate range:")
print("Min:", parsed_dates.min())
print("Max:", parsed_dates.max())

print("\n=== NUMERIC CONSISTENCY CHECK ===")
df["price_num"] = pd.to_numeric(df["price"], errors="coerce")
df["freight_num"] = pd.to_numeric(df["freight_value"], errors="coerce")

print("Invalid price:", df["price_num"].isna().sum())
print("Invalid freight_value:", df["freight_num"].isna().sum())

print("Negative price:", (df["price_num"] < 0).sum())
print("Negative freight_value:", (df["freight_num"] < 0).sum())

print("Zero price:", (df["price_num"] == 0).sum())
print("Zero freight_value:", (df["freight_num"] == 0).sum())

print("\n=== DESCRIPTIVE STATS ===")
print(df[["price_num", "freight_num"]].describe())