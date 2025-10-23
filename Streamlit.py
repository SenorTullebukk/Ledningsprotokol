import streamlit as st
from main_scepter import *
from main_ledning import *

st.set_page_config(
    page_title="Automatisk ledningsprotokol",
    layout="centered",
    page_icon="Billeder/N.png"
)

# Sidebar menu with navigation

# Define pages
pages = {
    "Ledningsprotokol": "Automatisk ledningsprotokol",
    "Scepterplacering": "Automatisk scepterplacering",
    'Guide': 'Guide',
}

# Sidebar toggle
with st.sidebar:
    st.image("Billeder/Logo.png", width=150)
    st.header("Menu")
    selected_page = st.radio("Vælg side", list(pages.keys()))

# Page content
if selected_page == "Ledningsprotokol":
    st.title(pages[selected_page])
    #Start_ledningsprogram()

elif selected_page == "Scepterplacering":
    st.title(pages[selected_page])
    #Start_Scepterplacering()
    
elif selected_page == 'Guide':
    st.title(pages[selected_page])
    st.write('''
             Beskrivelse af hvordan man bruger de forskellige funktioner i programmet.\\
             Det er vigtigt at man har referede de forskellige LER ind i en fil, dersom det er vigtigt at differencere imellem ledningsejere.\\
             Skriv en mail til JHAA hvis der er fejl, eller hvis du har forslag til forbedringer eller funktioner den mangler.
             ''')
    st.header('Batch konvertering af DGN til DXF')
    st.write('''
             En guide til hvordan man konvertere flere DGN filer til DXF filer på en gang.\\
             ''')