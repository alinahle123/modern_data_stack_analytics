import pandas as pd
import re
import unicodedata

# =========================================================
# 1. LOAD DATA
# =========================================================
df = pd.read_csv("C:/Users/Dell/Desktop/Datasets/Brazilian E-Commerce Public Dataset by Olist/olist_geolocation_dataset.csv")

print("====================================================")
print("OBSERVATION AUDIT - GEOLOCATION CITY CONSISTENCY")
print("====================================================")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")
print("\nColumns list:")
print(df.columns.tolist())

# =========================================================
# 2. BASIC QUALITY CHECKS
# =========================================================
print("\n=== NULL VALUES ===")
print(df[["geolocation_city", "geolocation_state"]].isna().sum())

print("\n=== BLANK STRING CHECK ===")
for col in ["geolocation_city", "geolocation_state"]:
    blank_count = df[col].astype(str).str.strip().eq("").sum()
    print(f"{col}: {blank_count}")

# =========================================================
# 3. NORMALIZATION FUNCTIONS FOR ANALYSIS ONLY
#    These are used only to COMPARE values, not to overwrite them.
# =========================================================
def remove_accents(text):
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c))

def normalize_for_analysis(text):
    """
    Observation-only normalization key.
    Used to detect whether multiple raw city values represent
    the same logical city after standardization.
    """
    if pd.isna(text):
        return None

    text = str(text)

    # raw text kept intact elsewhere, this is only an analysis key
    text = text.strip().lower()
    text = remove_accents(text)

    # replace common punctuation with spaces
    text = re.sub(r"['’`´\-_/(),.;:]", " ", text)

    # remove non-alphanumeric noise
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # collapse repeated spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text

# =========================================================
# 4. CREATE ANALYSIS COLUMNS
# =========================================================
df["city_raw"] = df["geolocation_city"].astype(str)
df["city_trimmed"] = df["city_raw"].str.strip()
df["city_analysis_key"] = df["city_raw"].apply(normalize_for_analysis)

# =========================================================
# 5. HIGH-LEVEL CONSISTENCY METRICS
# =========================================================
print("\n=== UNIQUE VALUE COMPARISON ===")
print("Unique raw city values:       ", df["city_raw"].nunique())
print("Unique trimmed city values:   ", df["city_trimmed"].nunique())
print("Unique analysis-key values:   ", df["city_analysis_key"].nunique())

print("\n=== WHAT THIS MEANS ===")
raw_unique = df["city_raw"].nunique()
trimmed_unique = df["city_trimmed"].nunique()
analysis_unique = df["city_analysis_key"].nunique()

print(f"Difference raw vs trimmed: {raw_unique - trimmed_unique}")
print(f"Difference raw vs analysis key: {raw_unique - analysis_unique}")

# =========================================================
# 6. WHITESPACE INCONSISTENCIES
# =========================================================
print("\n=== WHITESPACE INCONSISTENCIES ===")
leading_trailing_spaces = (df["city_raw"] != df["city_trimmed"]).sum()
multiple_internal_spaces = df["city_raw"].str.contains(r"\s{2,}", regex=True, na=False).sum()

print(f"Rows with leading/trailing spaces: {leading_trailing_spaces}")
print(f"Rows with multiple internal spaces: {multiple_internal_spaces}")

print("\nExamples with leading/trailing spaces:")
space_examples = df.loc[df["city_raw"] != df["city_trimmed"], "city_raw"].drop_duplicates().head(20)
print(space_examples.to_string(index=False))

# =========================================================
# 7. CASE INCONSISTENCIES
# =========================================================
print("\n=== CASE INCONSISTENCIES ===")
case_profile = pd.DataFrame({
    "raw": df["city_raw"],
    "lower": df["city_raw"].str.lower(),
    "upper": df["city_raw"].str.upper()
})

# A city has case inconsistency if the lowercase form maps to multiple raw spellings
case_variants = (
    df.groupby(df["city_raw"].str.lower())
      .agg(raw_variants=("city_raw", "nunique"), rows=("city_raw", "size"))
      .reset_index()
)
case_inconsistent = case_variants[case_variants["raw_variants"] > 1].sort_values(
    ["raw_variants", "rows"], ascending=[False, False]
)

print(f"Number of lowercase city groups with multiple case variants: {len(case_inconsistent)}")
print("\nTop 20 case-inconsistent groups:")
print(case_inconsistent.head(20).to_string(index=False))

# =========================================================
# 8. ACCENT / PUNCTUATION / ENCODING INCONSISTENCIES
# =========================================================
print("\n=== SEMANTIC TEXT INCONSISTENCIES DETECTED THROUGH ANALYSIS KEY ===")

variant_summary = (
    df.groupby("city_analysis_key")
      .agg(
          total_rows=("city_raw", "size"),
          raw_variants=("city_raw", "nunique")
      )
      .reset_index()
      .sort_values(["raw_variants", "total_rows"], ascending=[False, False])
)

inconsistent_groups = variant_summary[variant_summary["raw_variants"] > 1].copy()

print(f"Number of analysis-key groups with multiple raw variants: {len(inconsistent_groups)}")
print("\nTop 30 inconsistent groups:")
print(inconsistent_groups.head(30).to_string(index=False))

# =========================================================
# 9. SHOW RAW VARIANTS FOR THE MOST INCONSISTENT GROUPS
# =========================================================
print("\n=== RAW VARIANTS INSIDE THE MOST INCONSISTENT GROUPS ===")
top_groups = inconsistent_groups.head(20)["city_analysis_key"].tolist()

for key in top_groups:
    print("\n----------------------------------------------------")
    print(f"Analysis key: {key}")
    variants = df.loc[df["city_analysis_key"] == key, "city_raw"].value_counts().head(20)
    print(variants.to_string())

# =========================================================
# 10. SUSPICIOUS CHARACTER CHECK
# =========================================================
print("\n=== SUSPICIOUS CHARACTER CHECK ===")
suspicious_pattern = r"[^A-Za-zÀ-ÿ0-9\s'’`´\-/(),.;:]"
suspicious_rows = df[df["city_raw"].str.contains(suspicious_pattern, regex=True, na=False)]

print(f"Rows with suspicious characters in city: {len(suspicious_rows)}")
print("\nExamples:")
print(suspicious_rows["city_raw"].drop_duplicates().head(30).to_string(index=False))

# =========================================================
# 11. DIFFERENCE BETWEEN RAW VALUE AND ANALYSIS KEY
# =========================================================
print("\n=== EXAMPLES WHERE RAW VALUE DIFFERS FROM ANALYSIS KEY ===")
diff_examples = df.loc[
    df["city_raw"].str.strip().str.lower() != df["city_analysis_key"],
    ["city_raw", "city_analysis_key"]
].drop_duplicates().head(50)

print(diff_examples.to_string(index=False))

# =========================================================
# 12. OPTIONAL SUMMARY TABLE FOR DOCUMENTATION
# =========================================================
summary = {
    "total_rows": df.shape[0],
    "raw_unique_cities": df["city_raw"].nunique(),
    "trimmed_unique_cities": df["city_trimmed"].nunique(),
    "analysis_key_unique_cities": df["city_analysis_key"].nunique(),
    "rows_with_leading_trailing_spaces": int(leading_trailing_spaces),
    "rows_with_multiple_internal_spaces": int(multiple_internal_spaces),
    "case_inconsistent_groups": int(len(case_inconsistent)),
    "semantic_inconsistent_groups": int(len(inconsistent_groups)),
    "rows_with_suspicious_characters": int(len(suspicious_rows)),
}

summary_df = pd.DataFrame([summary])

print("\n=== SUMMARY TABLE ===")
print(summary_df.to_string(index=False))


