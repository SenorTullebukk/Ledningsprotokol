import streamlit as st
#from main import *

st.set_page_config(
    page_title="Automatisk ledningsprotokol",
    layout="centered",
    page_icon=r"Billeder/n.ico"
)

# Sidebar menu with navigation

# Define pages
pages = {
    "Ledningsprotokol": "Automatisk ledningsprotokol",
    "Scepterplacering": "Automatisk scepterplacering",
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
    #Startprogram()

elif selected_page == "Scepterplacering":
    st.title(pages[selected_page])
    #Scepterplacering()
    # Load the file content to be downloaded
    st.write("Der er pt. ikke nogen funktionalitet her, men det er planen at der skal være mulighed for at finde placeringer til septere automatisk.")
    with open("Diverse/ScepterScript.py", "r", encoding="utf-8") as f:
        file_content = f.read()
    st.download_button(
        label="Download Python script til MicroStation",
        data=file_content,
        file_name="ScepterScript.py",
        mime="text/x-python",
        disabled=False
    )

elif selected_page == "Om":
    st.title(pages[selected_page])
    st.write("Skriv en mail til JHAA hvis der er fejl, eller hvis du har forslag til forbedringer eller funktioner den mangler.")