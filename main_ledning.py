from Funktioner import *

def Start_ledningsprogram():    
    st.write('''
             Alle ledningsfiler og projektet skal uploades som .dxf. Guide her til at vise hvordan man kan lave en batch convertion. Derefter er det muligt at gå igennem programmet for at finde punkter til alle scepterplaceringerne.\\
             Den excel som scriptet genererer har i første ark placeringerne af alle scepterne, i andet ark de valgte respektafstande og sidste ark en kvalitetssikring for respektafstandende er overholdt.
             ''')
    uploaded_files = st.file_uploader("Geometri", type=["dxf"], help="Vælg en DXF-fil", accept_multiple_files=True)
    if uploaded_files:
        files = uploaded_files if isinstance(uploaded_files, list) else [uploaded_files]
        st.write(f"Modtog {len(files)} fil(er).")
    else:
        st.write("Ingen fil valgt")
