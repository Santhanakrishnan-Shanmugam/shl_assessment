import streamlit as st
import requests

st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 SHL Assessment Recommendation System")
st.markdown(
    """
Enter a query describing the type of assessments you are looking for.
For example: *"Looking for leadership and sales assessment for managers"*
"""
)

# User input
query = st.text_input("Enter your query here:")

if st.button("Get Recommendations") and query:
    with st.spinner("Fetching recommendations..."):
        try:
            response = requests.post(
                "http://127.0.0.1:8000/recommend", 
                json={"query": query}
            )
            response.raise_for_status()
            data = response.json()
            recommendations = data.get("results", [])

            if recommendations:
                st.success(f"Found {len(recommendations)} recommendations!")
                for rec in recommendations:
                    st.markdown(
                        f"""
                        ### {rec['name']}
                        **Category:** {rec['category']}  
                        **Test Type:** {rec['test_type']}  
                        [View Product]({rec['url']})
                        """
                    )
                    st.divider()
            else:
                st.warning("No recommendations found for your query.")

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to backend: {e}")
