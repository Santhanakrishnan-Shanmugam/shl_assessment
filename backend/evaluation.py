import pandas as pd
import recommender

# -----------------------------
# Load labeled train data
# -----------------------------
TRAIN_XLSX = "../Gen_AI Dataset.xlsx"
df = pd.read_excel(TRAIN_XLSX)
print("Columns in dataset:", df.columns)

# Extract assessment names from URLs
def extract_name(url):
    return url.rstrip("/").split("/")[-1].lower()

df['relevant_assessments'] = df['Assessment_url'].apply(
    lambda x: [extract_name(u) for u in x.split("|")] if isinstance(x, str) else [extract_name(x)]
)

# -----------------------------
# Metrics
# -----------------------------
def precision_at_k(preds, truths, k):
    top_k_preds = preds[:k]
    return len(set(top_k_preds) & set(truths)) / k

def recall_at_k(preds, truths, k):
    top_k_preds = preds[:k]
    return len(set(top_k_preds) & set(truths)) / len(truths)

def mrr(preds, truths):
    for idx, pred in enumerate(preds, start=1):
        if pred in truths:
            return 1 / idx
    return 0

# -----------------------------
# Evaluate
# -----------------------------
top_k = 5
precision_scores = []
recall_scores = []
mrr_scores = []

results_list = []

for i, row in df.iterrows():
    query = row['Query']
    truths = row['relevant_assessments']

    preds_dicts = recommender.recommend(query, top_k=top_k)
    preds = [extract_name(p['url']) for p in preds_dicts]

    print("Query:", query)
    print("Predictions (top 5):", preds)
    print("Ground truth:", truths)
    print("-"*50)

    # Metrics
    precision_scores.append(precision_at_k(preds, truths, top_k))
    recall_scores.append(recall_at_k(preds, truths, top_k))
    mrr_scores.append(mrr(preds, truths))

    # Save for CSV
    results_list.append({
        "Query": query,
        "Predictions": "|".join(preds),
        "Ground_truth": "|".join(truths)
    })

# -----------------------------
# Results
# -----------------------------
print(f"Precision@{top_k}: {sum(precision_scores)/len(precision_scores):.3f}")
print(f"Recall@{top_k}: {sum(recall_scores)/len(recall_scores):.3f}")
print(f"MRR: {sum(mrr_scores)/len(mrr_scores):.3f}")

# -----------------------------
# Save evaluation results
# -----------------------------
results_df = pd.DataFrame(results_list)
results_df.to_csv("evaluation_results.csv", index=False)
print("Saved evaluation_results.csv")
