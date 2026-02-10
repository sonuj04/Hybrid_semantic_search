import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer
import time
from dotenv import load_dotenv
import os


@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-mpnet-base-v2")

model = None

st.set_page_config(
    page_title="Fashion Semantic Search",
    page_icon="🛍️",
    layout="wide"
)


indexName = "all_products"

try:

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
    


def search(input_keyword,gender_filter,max_price):

    start_time = time.time()    
    global model
    if model is None:
        model = load_embedding_model()
    vector_of_input_keyword = model.encode(
        input_keyword,
        normalize_embeddings=True
    )

    # res = es.search(
    #     index="all_products",
    #     knn={
    #         "field": "DescriptionVector",
    #         "query_vector": vector_of_input_keyword,
    #         "k": 5,
    #         "num_candidates": 500
    #     },
    # _source=[
    #         "ProductName",
    #         "Description",
    #         "ProductBrand",
    #         "Price (INR)",
    #         "Gender"
    #     ]
    # )

    filters = []   #building filters

    if gender_filter != "ALL":
        filters.append({"term": {"Gender": gender_filter}})

    filters.append({
        "range": {
            "Price (INR)": {
                "lte": max_price
            }
        }
    })

    res = es.search(
        index="all_products",
        query={
            "bool": {
                "must": [
                    {
                        "multi_match": {
                            "query": input_keyword,
                            "fields": [
                                "ProductName^2",
                                "Description",
                                "ProductBrand",
                                "Gender"
                            ]
                        }
                    }
                ],
                "filter": filters
            }
        },
        knn={
            "field": "DescriptionVector",
            "query_vector": vector_of_input_keyword,
            "k": 10,
            "num_candidates": 1000
        },
        _source=[
            "ProductName",
            "Description",
            "ProductBrand",
            "Price (INR)",
            "Gender"
        ]
    )



    latency = time.time() - start_time
    results = res["hits"]["hits"]

    return results,latency

def main():
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 2.2rem;
            font-weight: 600;
            color: #1a73e8; /* Google Blue */
            margin-bottom: 0.2rem;
        }
        .subtitle {
            color: #5f6368;
            font-size: 1rem;
            margin-bottom: 1.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="main-title">Fashion Semantic Search</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Search products by meaning, not just keywords</div>',
        unsafe_allow_html=True
    )






    st.title("Search Fashion Products")

    #enter search query
    search_query = st.text_input(
        "",
        placeholder="e.g. black dress for women under 2000"

    )
    st.markdown("<hr style='margin-top:0.5rem; margin-bottom:1.5rem;'>", unsafe_allow_html=True)



    with st.sidebar:

        st.markdown(
            """
            <style>
            .sidebar-title {
                font-size: 1.1rem;
                font-weight: 600;
                color: #202124;
                margin-bottom: 0.8rem;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.markdown('<div class="sidebar-title">Filters</div>', unsafe_allow_html=True)



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
    if st.button("Search", type="primary"):
        if search_query:
            results,latency = search(search_query,gender_filter,max_price)
            st.caption(f"{latency*1000:.0f} ms · Hybrid Search")
    


            st.subheader("Search Results")
            if not results:
                st.warning("No matching results found, try lenient filters or a different query :(")
            else:
                for result in results:
                    source = result.get("_source", {})

                    with st.container():
                        st.markdown(
                            """
                            <div style="
                                background-color:#ffffff;
                                border:1px solid #e0e0e0;
                                border-radius:10px;
                                padding:16px;
                                margin-bottom:16px;
                            ">
                            """,
                            unsafe_allow_html=True
                        )

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

                        st.markdown("</div>", unsafe_allow_html=True)
                        st.divider()

                    
if __name__ == "__main__":
    main()