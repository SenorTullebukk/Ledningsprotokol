from Funktioner import *

def Start_Scepterplacering():    
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
    DS_respektafstande = pd.read_excel("Diverse/Respektafstand_DS.xlsx")

    gdfs = {}
    gdfs = load_uploaded_dxf_files(files) if 'files' in locals() else {}
    import matplotlib.pyplot as plt

    if not gdfs:
        st.write("Ingen geodataframes at plotte.")
    else:
        for name, gdf in gdfs.items():
            if gdf is None or gdf.empty:
                st.write(f"{name}: tom geodataframe.")
                continue
            if 'geometry' not in gdf:
                st.write(f"{name}: ingen 'geometry' kolonne.")
                continue
            fig, ax = plt.subplots(figsize=(6, 6))
            gdf.plot(ax=ax, color='none', edgecolor='black', linewidth=0.6)
            ax.set_title(f"{name} — {len(gdf)} features")
            ax.axis('off')
            st.pyplot(fig)
    st.write(f"Indlæst {len(gdfs)} geodataframe(s).")