from Funktioner import *
import streamlit as st
import tempfile

def main():
    # Kør først Startprogram
    Startprogram()
    # Når Startprogram er færdig, kør andet_program automatisk
    andet_program()


def Startprogram():
    st.subheader("Vælg MicroStation DGN fil")

    uploaded_file = st.file_uploader(
        "Upload MicroStation DGN fil",
        type=["dgn"]
    )
    if uploaded_file is not None:
        # Save uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".dgn") as tmp_file:
            tmp_file.write(uploaded_file.read())
            dgn_path = tmp_file.name

        mspy_script_path = "MsPy_fil.py"

        # Add a button to confirm before proceeding
        if st.button("Kør"):
            # Run the processing function
            print('no')
            run_mspython_on_dgn(
            dgn_path=dgn_path,
            mspy_script_path=mspy_script_path,
            read_only=True,
            visible=True,
            wait_timeout_s=600,
            autosave=False
            )
            

def andet_program():
    st.write("Andet program funktionalitet kan tilføjes her.")
