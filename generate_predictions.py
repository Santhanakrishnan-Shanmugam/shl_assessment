
import csv
from backend.recommender import recommend

test_queries = [
    "I am hiring for Java developers who can collaborate effectively",
    "Looking to hire Python SQL JavaScript developers"
]

with open("predictions.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Query", "Assessment_url"])

    for q in test_queries:
        recs = recommend(q)
        for r in recs:
            writer.writerow([q, r["url"]])

