import pandas as pd

df = pd.read_csv("C:/Users/Dell/Desktop/Datasets/Brazilian E-Commerce Public Dataset by Olist/olist_products_dataset.csv")

print("=== BASIC SHAPE ===")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(df.columns.tolist())

print("\n=== NULL CHECK ===")
print(df.isna().sum())

print("\n=== DUPLICATE CHECK ===")
print(f"Exact duplicate rows: {df.duplicated().sum()}")
print(f"Duplicated product_id: {df['product_id'].duplicated().sum()}")

print("\n=== TEXT CLEANLINESS CHECK ===")
for col in ["product_id", "product_category_name"]:
    s = df[col].dropna().astype(str)
    print(f"{col} - leading/trailing spaces: {(s != s.str.strip()).sum()}")
    print(f"{col} - empty after strip: {(s.str.strip() == '').sum()}")

print("\n=== MISSING CATALOG BLOCK CHECK ===")
catalog_cols = [
    "product_category_name",
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty"
]

all_catalog_null = df[catalog_cols].isna().all(axis=1)
print(f"Rows where all catalog fields are null together: {all_catalog_null.sum()}")

if all_catalog_null.sum() > 0:
    print("\nSample rows with all catalog fields missing:")
    print(df.loc[all_catalog_null, ["product_id"] + catalog_cols].head(10).to_string(index=False))

print("\n=== NUMERIC FIELD CHECK ===")
num_cols = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

for col in num_cols:
    s = pd.to_numeric(df[col], errors="coerce")
    print(f"\n{col}")
    print(f"  nulls: {(s.isna()).sum()}")
    print(f"  zeros: {(s == 0).sum()}")
    print(f"  negatives: {(s < 0).sum()}")
    print(f"  min: {s.min()}")
    print(f"  max: {s.max()}")

print("\n=== PHYSICAL ATTRIBUTES CHECK ===")
phys_cols = [
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

all_phys_null = df[phys_cols].isna().all(axis=1)
print(f"Rows where all physical attributes are null together: {all_phys_null.sum()}")

if all_phys_null.sum() > 0:
    print("\nRows with all physical attributes missing:")
    print(df.loc[all_phys_null, ["product_id"] + phys_cols].to_string(index=False))

zero_weight = df[df["product_weight_g"] == 0]
print(f"\nRows with product_weight_g = 0: {len(zero_weight)}")

if not zero_weight.empty:
    print(zero_weight[["product_id"] + phys_cols].to_string(index=False))

print("\n=== CATEGORY COVERAGE ===")
print(df["product_category_name"].value_counts(dropna=False).head(20))

print("\n=== OBSERVATION SUMMARY ===")
print("1. The file has no duplicates and product_id is unique.")
print("2. product_id and product_category_name do not contain spacing issues.")
print("3. 610 rows are missing category and the same catalog metadata fields together.")
print("4. 2 rows are missing all physical attributes.")
print("5. 4 rows have weight equal to 0, which is likely not analytically reliable.")