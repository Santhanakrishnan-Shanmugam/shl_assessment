import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from pathlib import Path
# =========================
# CONFIG
# =========================
INDEX_DIR = Path(__file__).resolve().parent.parent / "data" / "faiss_store"
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# =========================
# LOAD EMBEDDING MODEL
# =========================
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004"
)

# =========================
# LOAD FAISS VECTOR STORE
# =========================
vectorstore = FAISS.load_local(
    INDEX_DIR,
    embeddings,
    allow_dangerous_deserialization=True
)

# =========================
# RECOMMEND FUNCTION
# =========================
def recommend(query: str, top_k: int = 5):
    docs = vectorstore.similarity_search(query, k=top_k)

    results = []
    for doc in docs:
        meta = doc.metadata
        results.append({
            "name": meta["name"],
            "url": meta["url"],
            "category": meta["category"],
            "test_type": meta["test_type"]
        })

    return results


# =========================
# LOCAL TEST
# =========================
# if __name__ == "__main__":
#     query = "I want to assess problem solving and logical reasoning skills"
#     recs = recommend(query)

#     for r in recs:
#         print(f"- {r['name']} ({r['test_type']}) → {r['url']}")
