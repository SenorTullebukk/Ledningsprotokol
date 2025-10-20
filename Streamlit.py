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
        for uploaded in files:
            st.write(uploaded.name)
            try:
                content = uploaded.read()
                st.write(f"Størrelse: {len(content)} bytes")
                uploaded.seek(0)
            except Exception as e:
                st.write("Kunne ikke læse fil:", e)
    else:
        st.write("Ingen fil valgt")
    
    import os
    script_path = "Diverse/ScepterScript.py"
    if os.path.exists(script_path):
        with open(script_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        st.download_button(
            label="Download Python script til MicroStation",
            data=file_content,
            file_name="ScepterScript.py",
            mime="text/x-python",
        )
    else:
        st.warning(f"Kunne ikke finde scriptet: {script_path}")
        st.download_button(
            label="Download Python script til MicroStation",
            data="",
            file_name="ScepterScript.py",
            mime="text/x-python",
            disabled=True
        )

elif selected_page == 'Guide':
    st.title(pages[selected_page])
    st.write('''
             Beskrivelse af hvordan man bruger de forskellige funktioner i programmet.\\
             Det er vigtigt at man har referede de forskellige LER ind i en fil, dersom det er vigtigt at differencere imellem ledningsejere.\\
             Skriv en mail til JHAA hvis der er fejl, eller hvis du har forslag til forbedringer eller funktioner den mangler.
             ''')