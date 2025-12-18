import os
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.schema import Document
from dotenv import load_dotenv
# =========================
# CONFIG
# =========================
DATA_PATH = "../data/shl_expanded.csv"
INDEX_DIR = "../data/faiss_store"



load_dotenv()  # loads .env file

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(DATA_PATH)

documents = []
for _, row in df.iterrows():
    documents.append(
        Document(
            page_content=row["llm_enriched_text"],
            metadata={
                "name": row["name"],
                "url": row["url"],
                "category": row["category"],
                "test_type": row["test_type"]
            }
        )
    )

# =========================
# EMBEDDINGS
# =========================
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004"
)

# =========================
# BUILD & SAVE FAISS INDEX
# =========================
vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local(INDEX_DIR)

print("✅ FAISS index built and saved successfully")
