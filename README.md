SHL Assessment Recommendation System
Project Overview

This project is a recommendation engine for SHL assessments. Given a user query describing a hiring need, the system recommends the most relevant assessments from the SHL catalog.

Backend: Python + FastAPI

Frontend: Streamlit

Vector Search: FAISS (for embedding-based similarity)

Evaluation: Precision, Recall, MRR

Data Preparation

Crawled SHL Assessment catalog using Python (requests + BeautifulSoup).

Dataset contains 377+ Individual Test Solutions with:

name

url

category

test_type

Labeled train data provided for evaluation:

Queries + relevant assessment URLs.

Backend

recommender.py:

Builds embeddings for assessments.

Stores them in FAISS vectorstore.

Provides a recommend(query, top_k=5) function.

main.py:

FastAPI server to serve recommendations.

Accepts POST requests with query and returns top 5 assessments.

Frontend

Streamlit app allows users to:

Input a hiring query.

Display top 5 recommended assessments with names and URLs.

Frontend interacts with FastAPI backend.

Evaluation

Script: evaluation.py

Metrics:

Precision@K: Fraction of top-K recommendations that are relevant.

Recall@K: Fraction of relevant items retrieved in top-K.

MRR (Mean Reciprocal Rank): Average reciprocal rank of the first relevant item.

Train data is used to measure system performance and iterate if necessary.

Sample Output:

Metric	Value
Precision@5	0.009
Recall@5	0.046
MRR	0.026

Predictions and ground truth comparison are saved in evaluation_results.csv.

How to Run

Install dependencies:

pip install -r requirements.txt


Run Backend:

cd backend
uvicorn main:app --reload


Run Frontend:

streamlit run frontend/app.py


Evaluate system:

python backend/evaluation.py


This will print metrics and generate evaluation_results.csv.

Improvement Notes

Metrics are low because of:

Broad queries vs. niche assessments.

Limited retrieval and ranking logic (FAISS is embedding-based only).

Possible enhancements:

Add keyword-based reranking.

Expand training data or embeddings with description text of assessments.

Use hybrid retrieval (embedding + keyword matching).

Submission Contents

backend/: Python backend + recommender + evaluation script

frontend/: Streamlit frontend

evaluation_results.csv: Evaluation predictions vs. ground truth

README.md: Project overview and instructions"# shl_assessment" 
