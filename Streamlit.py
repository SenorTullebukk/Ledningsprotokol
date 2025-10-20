import streamlit as st
#from main import *

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
    #Startprogram()

elif selected_page == "Scepterplacering":
    st.title(pages[selected_page])
    #Scepterplacering()
    # Load the file content to be downloaded
    st.write('''
             Der er pt. ikke nogen funktionalitet her, men det er planen at der skal være mulighed for at finde placeringer til septere automatisk.\\
             Jeg mangler lige en ABC til hvad som skal være resultatet, af scriptet.
             ''')
    
    uploaded_files = st.file_uploader("Geometri", type=["dxf"], help="Vælg en DXF-fil", accept_multiple_files=True)
    if uploaded_files:
        files = uploaded_files if isinstance(uploaded_files, list) else [uploaded_files]
        st.write(f"Modtog {len(files)} fil(er):")
    else:
        st.write("Ingen fil valgt")
    
elif selected_page == 'Guide':
    st.title(pages[selected_page])
    st.write('''
             Beskrivelse af hvordan man bruger de forskellige funktioner i programmet.\\
             Det er vigtigt at man har referede de forskellige LER ind i en fil, dersom det er vigtigt at differencere imellem ledningsejere.\\
             Skriv en mail til JHAA hvis der er fejl, eller hvis du har forslag til forbedringer eller funktioner den mangler.
             ''')