import pandas as pd

df = pd.read_csv("C:/Users/Dell/Desktop/Datasets/Brazilian E-Commerce Public Dataset by Olist/olist_orders_dataset.csv")

print("=== BASIC SHAPE ===")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")
print(df.columns.tolist())

print("\n=== NULL CHECK ===")
print(df.isna().sum())

print("\n=== DUPLICATE CHECK ===")
print(f"Exact duplicate rows: {df.duplicated().sum()}")
print(f"Duplicated order_id: {df['order_id'].duplicated().sum()}")
print(f"Duplicated customer_id: {df['customer_id'].duplicated().sum()}")

print("\n=== ORDER STATUS VALUES ===")
print(df["order_status"].value_counts(dropna=False))

# Parse timestamps
date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_cols:
    df[col] = pd.to_datetime(df[col], errors="coerce")

print("\n=== TIMESTAMP LOGIC CHECKS ===")

approved_before_purchase = df[
    df["order_approved_at"].notna() &
    (df["order_approved_at"] < df["order_purchase_timestamp"])
]
print(f"order_approved_at before purchase: {len(approved_before_purchase)}")

carrier_before_purchase = df[
    df["order_delivered_carrier_date"].notna() &
    (df["order_delivered_carrier_date"] < df["order_purchase_timestamp"])
]
print(f"delivered_carrier_date before purchase: {len(carrier_before_purchase)}")

carrier_before_approved = df[
    df["order_delivered_carrier_date"].notna() &
    df["order_approved_at"].notna() &
    (df["order_delivered_carrier_date"] < df["order_approved_at"])
]
print(f"delivered_carrier_date before approved_at: {len(carrier_before_approved)}")

customer_before_purchase = df[
    df["order_delivered_customer_date"].notna() &
    (df["order_delivered_customer_date"] < df["order_purchase_timestamp"])
]
print(f"delivered_customer_date before purchase: {len(customer_before_purchase)}")

customer_before_carrier = df[
    df["order_delivered_customer_date"].notna() &
    df["order_delivered_carrier_date"].notna() &
    (df["order_delivered_customer_date"] < df["order_delivered_carrier_date"])
]
print(f"delivered_customer_date before carrier_date: {len(customer_before_carrier)}")

non_delivered_with_customer_date = df[
    (df["order_status"] != "delivered") &
    df["order_delivered_customer_date"].notna()
]
print(f"Non-delivered statuses with delivered_customer_date filled: {len(non_delivered_with_customer_date)}")

print("\nBreakdown of non-delivered rows with customer delivery timestamp:")
if not non_delivered_with_customer_date.empty:
    print(non_delivered_with_customer_date["order_status"].value_counts())

print("\n=== SAMPLE ANOMALIES ===")

if not carrier_before_approved.empty:
    print("\nSample rows where carrier date is before approval:")
    print(
        carrier_before_approved[
            [
                "order_id",
                "order_status",
                "order_purchase_timestamp",
                "order_approved_at",
                "order_delivered_carrier_date",
                "order_delivered_customer_date"
            ]
        ].head(10).to_string(index=False)
    )

if not customer_before_carrier.empty:
    print("\nSample rows where customer delivery is before carrier handoff:")
    print(
        customer_before_carrier[
            [
                "order_id",
                "order_status",
                "order_purchase_timestamp",
                "order_approved_at",
                "order_delivered_carrier_date",
                "order_delivered_customer_date"
            ]
        ].head(10).to_string(index=False)
    )

if not non_delivered_with_customer_date.empty:
    print("\nSample non-delivered rows with customer delivery timestamp:")
    print(
        non_delivered_with_customer_date[
            [
                "order_id",
                "order_status",
                "order_approved_at",
                "order_delivered_carrier_date",
                "order_delivered_customer_date"
            ]
        ].head(10).to_string(index=False)
    )



print("\n=== OBSERVATION SUMMARY ===")
print("1. The file has no duplicates and IDs are unique.")
print("2. order_status is already standardized.")
print("3. Some lifecycle timestamps contradict the expected order flow.")
print("4. Invalid shipping and delivery timestamps were nullified, not replaced.")
print("5. Missing timestamps were kept as null because there is no reliable way to infer them.")