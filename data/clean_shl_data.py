import pandas as pd

INPUT_CSV = "../crawler/shl_product_links_enriched.csv"
OUTPUT_CSV = "../data/shl_clean.csv"

df = pd.read_csv(INPUT_CSV)

# Remove rows with no name or description
df = df.dropna(subset=["name", "description"])
df = df[df["name"].str.strip() != ""]

# Deduplicate by URL
df = df.drop_duplicates(subset=["url"])

# Infer test type
def infer_test_type(text):
    text = text.lower()
    if any(k in text for k in ["personality", "behavior", "motivation"]):
        return "P"
    return "K"

df["test_type"] = df["description"].apply(infer_test_type)

# Add category placeholder
df["category"] = "Individual Test Solution"

df.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Cleaned data saved: {len(df)} rows")
