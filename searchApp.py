import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

@st.cache_resource
def load_embedding_model():
    print("loading model")
    return SentenceTransformer("all-mpnet-base-v2")

model = load_embedding_model()

indexName = "all_products"

try:
    from dotenv import load_dotenv
    import os

    load_dotenv()  

    es = Elasticsearch(
        os.environ["ES_URL"],
        basic_auth=(
            os.environ["ES_USERNAME"],
            os.environ["ES_PASSWORD"]
        ),
        ca_certs=os.environ["ES_CA_CERT"]
    )
except ConnectionError as e:
    print("Connection Error:", e)
    
if es.ping():
    print("Successfully connected to ElasticSearch!!")
else:
    print("Oops!! Can not connect to Elasticsearch!")




def search(input_keyword):
    vector_of_input_keyword = model.encode(input_keyword)

    res = es.search(
        index="all_products",
        knn={
            "field": "DescriptionVector",
            "query_vector": vector_of_input_keyword,
            "k": 2,
            "num_candidates": 500
        },
    _source=["ProductName", "Description"]
    )
    results = res["hits"]["hits"]

    return results

def main():
    st.title("Search Fashion Products")

    # Input: User enters search query
    search_query = st.text_input("Enter your search query")

    # Button: User triggers the search
    if st.button("Search"):
        if search_query:
            # Perform the search and get results
            results = search(search_query)

            # Display search results
            st.subheader("Search Results")
            for result in results:
                with st.container():
                    if '_source' in result:
                        try:
                            st.header(f"{result['_source']['ProductName']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.write(f"Description: {result['_source']['Description']}")
                        except Exception as e:
                            print(e)
                        st.divider()

                    
if __name__ == "__main__":
    main()