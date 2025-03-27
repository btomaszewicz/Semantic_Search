import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Movie Title Search",
    page_icon="🎬",
    layout="centered"
)

# App header
st.title("🎬 Movie Title Search")
st.subheader("Find movies by describing their plots")

# Description
st.markdown("""
Enter a description of a movie plot or themes you're looking for,
and we'll find the closest matches for you!
""")

# Search input
with st.form(key="search_form"):
    query = st.text_area(
        "Describe the plot or themes you're interested in:",
        placeholder="Example: A dystopian future where people live in a simulated reality",
        height=100
    )
    submit_button = st.form_submit_button(label="Search Movies")

# Footer
st.markdown("---")
st.markdown(
    "This is a semantic movie search engine that helps you find movies "
    "based on plot descriptions. It uses natural language processing to understand "
    "your query and find the most relevant matches."
)
