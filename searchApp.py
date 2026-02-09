import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

@st.cache_resource
def load_embedding_model():
    print("loading model")
    return SentenceTransformer("all-mpnet-base-v2")

model = load_embedding_model()

st.set_page_config(
    page_title="Fashion Semantic Search",
    page_icon="🛍️",
    layout="wide"
)


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
    vector_of_input_keyword = model.encode(
        input_keyword,
        normalize_embeddings=True
    )

    res = es.search(
        index="all_products",
        knn={
            "field": "DescriptionVector",
            "query_vector": vector_of_input_keyword,
            "k": 5,
            "num_candidates": 500
        },
    _source=[
            "ProductName",
            "Description",
            "ProductBrand",
            "Price (INR)",
            "Gender"
        ]
    )
    results = res["hits"]["hits"]

    return results

def main():
    st.title("Search Fashion Products")

    #senter search query
    search_query = st.text_input(
        "Search your fave fashion products",
        placeholder="e.g. black dress for women under 2000"
    )
    with st.sidebar:
        st.header("Filters")

        gender_filter = st.selectbox(
            "Gender",
            ["All", "Men", "Women", "Unisex"]
        )

        max_price = st.slider(
            "Max Price (₹)",
            min_value=500,
            max_value=10000,
            step=500,
            value=5000
        )   


    # Button
    if st.button("Search"):
        if search_query:
            results = search(search_query)


            filtered_results = []

            for result in results:
                src = result.get("_source", {})


                if gender_filter != "All" and src.get("Gender") != gender_filter:
                    continue


                if src.get("Price (INR)", 0) > max_price:
                    continue

                filtered_results.append(result)


            st.subheader("Search Results")
            if not filtered_results:
                st.warning("No products matched your filters :()")
            else:
                for result in filtered_results:
                    source = result.get("_source", {})
                    with st.container():
            
                        st.subheader(source.get("ProductName", "Unknown Product"))
                        col1, col2 = st.columns([1, 2])

                        with col1:
                            st.caption("Brand")
                            st.write(source.get("ProductBrand", "N/A"))

                            st.caption("Gender")
                            st.write(source.get("Gender", "N/A"))

                            st.caption("Price")
                            st.markdown(
                                f"<h4 style='color:#2E86C1;'>₹{source.get('Price (INR)', 'N/A')}</h4>",
                                unsafe_allow_html=True
                            )

                        with col2:
                            st.caption("Description")
                            st.write(source.get("Description", "No description available"))

                        st.divider()

                    
if __name__ == "__main__":
    main()