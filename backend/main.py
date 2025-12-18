from fastapi import FastAPI
from pydantic import BaseModel
from recommender import recommend

app = FastAPI(
    title="SHL Assessment Recommendation API",
    description="AI-powered SHL test recommender using FAISS + Gemini",
    version="1.0.0"
)

# =========================
# REQUEST SCHEMA
# =========================
class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def health():
    return {"status": "SHL Recommendation API running"}

# =========================
# RECOMMEND ENDPOINT
# =========================
@app.post("/recommend")
def get_recommendations(req: QueryRequest):
    results = recommend(req.query, req.top_k)
    return {
        "query": req.query,
        "results": results
    }
