import streamlit as st
from main import *

st.set_page_config(
    page_title="Automatisk ledningsprotokol",
    layout="centered",
    page_icon=r"Billeder/n.ico"
)

# Sidebar menu with navigation

# Define pages
pages = {
    "Ledningsprotokol": "Automatisk ledningsprotokol",
    "Om": "Om",
}

# Sidebar toggle
with st.sidebar:
    st.image("Billeder/Logo.png", width=150)
    st.header("Menu")
    selected_page = st.radio("Vælg side", list(pages.keys()))

# Page content
if selected_page == "Ledningsprotokol":
    st.title(pages[selected_page])
    #main()


elif selected_page == "Om":
    st.title(pages[selected_page])
    st.write("Skriv en mail til JHAA hvis der er fejl, eller hvis du har forslag til forbedringer eller funktioner den mangler.")

