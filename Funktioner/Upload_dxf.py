from Funktioner import *

def load_uploaded_dxf_files(uploaded_list):
        gdfs_local = {}
        for uploaded in uploaded_list:
            suffix = os.path.splitext(uploaded.name)[1] or ".dxf"
            tmp_path = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded.read())
                    tmp.flush()
                    tmp_path = tmp.name
                gdf = gpd.read_file(tmp_path)
                gdf.attrs["source_file"] = uploaded.name
                gdfs_local[uploaded.name] = gdf
            except Exception as e:
                st.error(f"Kunne ikke læse {uploaded.name}: {e}")
            finally:
                if tmp_path and os.path.exists(tmp_path):
                    os.remove(tmp_path)
        return gdfs_local