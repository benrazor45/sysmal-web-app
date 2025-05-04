import streamlit as st

def upload_page():
    st.header("Upload File")
    uploaded_file = st.file_uploader("Upload file EXE untuk dianalisis", type=["exe"])
    if uploaded_file:
        st.success(f"File {uploaded_file.name} berhasil diupload.")