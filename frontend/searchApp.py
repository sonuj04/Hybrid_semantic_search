import streamlit as st
import requests

#config
API_URL = "http://localhost:8000/search"  

st.set_page_config(
    page_title="Fashion Semantic Search",
    layout="wide"
)



st.markdown("""
<style>
.main-title {
    font-size: 2.2rem;
    font-weight: 600;
    color: #1a73e8;
    margin-bottom: 0.2rem;
}
.subtitle {
    color: #5f6368;
    margin-bottom: 1.5rem;
}
.card {
    background-color: white;
    border: 1px solid #e0e0e0;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
}
.price {
    color: #34a853;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Fashion Semantic Search</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Search products by meaning, not just keywords</div>', unsafe_allow_html=True)





#search inputs
search_query = st.text_input(
    "",
    placeholder="e.g. black dress for women under 2000"
)


with st.sidebar:
    st.header("Filters")

    gender_filter = st.selectbox(
        "Gender",
        ["ALL", "Men", "Women", "Unisex"]
    )

    max_price = st.slider(
        "Max Price (₹)",
        min_value=500,
        max_value=10000,
        step=500,
        value=5000
    )

#button
if st.button("Search", type="primary"):

    if not search_query:
        st.warning("Please enter a search query.")
    else:
        try:
            payload = {
                "query": search_query,
                "gender": None if gender_filter == "ALL" else gender_filter,
                "max_price": max_price
            }

            response = requests.post(API_URL, json=payload)

            if response.status_code != 200:
                st.error(f"Backend error: {response.text}")
            else:
                data = response.json()
                results = data.get("results", [])
                latency = data.get("latency_ms", 0)

                st.caption(f"Search time: {latency:.2f} ms")

                if not results:
                    st.warning("No results found.")
                else:
                    st.subheader("Search Results")

                    # Show two results per row
                    for i in range(0, len(results), 2):
                        cols = st.columns(2)

                        for col, result in zip(cols, results[i:i+2]):
                            with col:
                                st.markdown('<div class="card">', unsafe_allow_html=True)

                                st.subheader(result.get("ProductName", "Unknown Product"))

                                st.write("Brand:", result.get("ProductBrand", "N/A"))
                                st.write("Gender:", result.get("Gender", "N/A"))

                                st.markdown(
                                    f'<div class="price">₹ {result.get("Price", "N/A")}</div>',
                                    unsafe_allow_html=True
                                )

                                st.write(result.get("Description", ""))

                                st.markdown('</div>', unsafe_allow_html=True)

        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to backend. Is FastAPI running?")
