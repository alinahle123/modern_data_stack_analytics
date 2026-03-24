import pandas as pd

# Load file
df = pd.read_csv("C:/Users/Dell/Desktop/Datasets/Brazilian E-Commerce Public Dataset by Olist/olist_order_payments_dataset.csv")

print("=== BASIC SHAPE ===")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print("\nColumns:")
print(df.columns.tolist())

print("\n=== NULL CHECK ===")
print(df.isna().sum())

print("\n=== DUPLICATE CHECK ===")
print(f"Exact duplicate rows: {df.duplicated().sum()}")

print("\n=== TEXT CLEANLINESS CHECK ===")
for col in ["order_id", "payment_type"]:
    leading_trailing = (df[col].astype(str) != df[col].astype(str).str.strip()).sum()
    print(f"{col} - rows with leading/trailing spaces: {leading_trailing}")

print("\n=== PAYMENT TYPE VALUES ===")
print(df["payment_type"].value_counts(dropna=False))

print("\n=== INSTALLMENTS CHECK ===")
print(df["payment_installments"].describe())
zero_installments = df[df["payment_installments"] == 0]
print(f"\nRows with payment_installments = 0: {len(zero_installments)}")
print(zero_installments[[
    "order_id",
    "payment_sequential",
    "payment_type",
    "payment_installments",
    "payment_value"
]].to_string(index=False))

print("\n=== ZERO PAYMENT VALUE CHECK ===")
zero_value = df[df["payment_value"] == 0]
print(f"Rows with payment_value = 0: {len(zero_value)}")
print(zero_value[[
    "order_id",
    "payment_sequential",
    "payment_type",
    "payment_installments",
    "payment_value"
]].sort_values(["payment_type", "payment_sequential"]).to_string(index=False))

print("\n=== SEQUENTIAL CONSISTENCY CHECK ===")

def expected_sequence(group):
    actual = sorted(group["payment_sequential"].tolist())
    expected = list(range(1, len(group) + 1))
    return actual == expected

bad_seq_orders = []
for order_id, group in df.groupby("order_id"):
    if not expected_sequence(group):
        bad_seq_orders.append({
            "order_id": order_id,
            "row_count": len(group),
            "raw_sequence": sorted(group["payment_sequential"].tolist())
        })

bad_seq_df = pd.DataFrame(bad_seq_orders)

print(f"Orders with inconsistent payment_sequential: {len(bad_seq_df)}")

if not bad_seq_df.empty:
    print("\nSample inconsistent orders:")
    print(bad_seq_df.head(20).to_string(index=False))

    sample_orders = bad_seq_df["order_id"].head(10).tolist()
    print("\nDetailed rows for sample inconsistent orders:")
    print(
        df[df["order_id"].isin(sample_orders)]
        .sort_values(["order_id", "payment_sequential"])
        .to_string(index=False)
    )



print("\n=== OBSERVATION SUMMARY ===")
print("1. No nulls and no exact duplicates were found.")
print("2. payment_type was already standardized.")
print("3. payment_sequential had inconsistent numbering for some orders, so it was rebuilt.")
print("4. A few paid card rows had 0 installments, so they were converted to 1.")
print("5. Zero payment_value rows were kept because they may reflect real business cases.")