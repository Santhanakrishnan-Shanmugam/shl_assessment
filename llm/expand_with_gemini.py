import os
import time
import json
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI

# ---------------- CONFIG ----------------
INPUT_CSV = "../data/shl_clean.csv"
OUTPUT_CSV = "../data/shl_expanded.csv"

# ✅ API key via environment (DO NOT hardcode in real projects)
# set GOOGLE_API_KEY in terminal if possible
# export GOOGLE_API_KEY=xxxx
# setx GOOGLE_API_KEY "xxxx" (Windows)
os.environ["GOOGLE_API_KEY"] ="AIzaSyDdQ5I-y2H8tsXXwYPvTPplR2iMols4VFI"

# ---------------- LLM ----------------
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",   # stable & supported
    temperature=0
)

# ---------------- PROMPT ----------------
PROMPT = """
You are an expert HR assessment consultant.

Return ONLY valid JSON in the following format.
No explanation. No markdown.


  "description": "...",
  "skills": ["..."],
  "roles": ["..."],
  "keywords": ["..."]


Assessment Name: {name}
Assessment Type: {test_type}
Assessment Description: {description}
"""

# ---------------- LOAD DATA ----------------
df = pd.read_csv(INPUT_CSV)
rows = []
#print(df)
# ---------------- PROCESS ----------------
for i, r in df.iterrows():
    print(f"🔹 Enriching {i+1}/{len(df)}: {r['name']}")

    prompt = PROMPT.format(
        name=r["name"],
        test_type=r["test_type"],
        description=r["description"]
    )

    try:
        response = model.invoke(prompt)

        # 🔒 Safe JSON extraction
        content = response.content.strip()
        content = content[content.find("{"):content.rfind("}") + 1]
        data = json.loads(content)

    except Exception as e:
        print(f"⚠️ JSON failed for {r['name']} → using fallback")
        data = {
            "description": r["description"],
            "skills": [],
            "roles": [],
            "keywords": []
        }

    # ---------------- ENRICHED TEXT ----------------
    enriched_text = (
        f"Assessment Name: {r['name']}\n"
        f"Assessment Type: {r['test_type']}\n"
        f"Category: {r['category']}\n\n"
        f"Overview: {data['description']}\n\n"
        f"Skills Measured: {', '.join(data['skills'])}\n"
        f"Relevant Roles: {', '.join(data['roles'])}\n"
        f"Keywords: {', '.join(data['keywords'])}"
    )

    rows.append({
        "name": r["name"],
        "url": r["url"],
        "category": r["category"],
        "test_type": r["test_type"],
        "llm_enriched_text": enriched_text
    })

    time.sleep(1)  # rate-limit safe

# ---------------- SAVE ----------------
pd.DataFrame(rows).to_csv(OUTPUT_CSV, index=False)
print("✅ LLM enrichment completed successfully")
