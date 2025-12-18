import os
import faiss
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# =========================
# CONFIG
# =========================
DATA_PATH = "../crawler/shl_product_links_enriched.csv"
INDEX_PATH = "../data/faiss.index"
load_dotenv()
# Make sure API key is set
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# =========================
# EMBEDDING MODEL
# =========================
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004"
)

def get_embedding(text: str) -> np.ndarray:
    emb = embedding_model.embed_query(text)
    return np.array(emb, dtype="float32")

# =========================
# BUILD FAISS INDEX
# =========================
def build_faiss_index():
    df = pd.read_csv(DATA_PATH)

    embeddings = []
    for text in df["llm_enriched_text"]:
        embeddings.append(get_embedding(text))

    embeddings = np.vstack(embeddings)
    dim = embeddings.shape[1]

    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    print(f"✅ FAISS index saved")
    print(f"🔢 Total vectors indexed: {index.ntotal}")
    print(f"📐 Embedding dimension: {dim}")

if __name__ == "__main__":
    build_faiss_index()
