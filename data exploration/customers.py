import pandas as pd

# Load file
df = pd.read_csv("C:/Users/Dell/Desktop/Datasets/Brazilian E-Commerce Public Dataset by Olist/olist_customers_dataset.csv")

print("=== BASIC OVERVIEW ===")
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\n=== NULL CHECK ===")
print(df.isna().sum())

print("\n=== EMPTY STRING CHECK ===")
for col in df.columns:
    if df[col].dtype == "object":
        empty_count = df[col].astype(str).str.strip().eq("").sum()
        print(f"{col}: {empty_count}")

print("\n=== EXACT DUPLICATES ===")
print("Duplicate rows:", df.duplicated().sum())

print("\n=== BUSINESS KEY CHECK ===")
print("Duplicate customer_id:", df["customer_id"].duplicated().sum())
print("Duplicate customer_unique_id:", df["customer_unique_id"].duplicated().sum())

print("\n=== WHITESPACE CHECK ON TEXT COLUMNS ===")
text_cols = ["customer_id", "customer_unique_id", "customer_city", "customer_state"]
for col in text_cols:
    leading_trailing_spaces = (df[col].astype(str) != df[col].astype(str).str.strip()).sum()
    print(f"{col}: {leading_trailing_spaces}")

print("\n=== CASE CONSISTENCY CHECK ===")
print("customer_city sample raw values:")
print(df["customer_city"].dropna().astype(str).head(10).tolist())

print("\nUnique customer_state formats:")
print(df["customer_state"].dropna().astype(str).str.len().value_counts().sort_index())

print("\n=== ZIP PREFIX FORMAT CHECK ===")
zip_as_str = df["customer_zip_code_prefix"].astype(str)
print("Min length:", zip_as_str.str.len().min())
print("Max length:", zip_as_str.str.len().max())
print("Examples of ZIPs with length < 5:")
print(zip_as_str[zip_as_str.str.len() < 5].head(10).tolist())