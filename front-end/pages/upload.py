import streamlit as st
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='C:/Users/USER/sysmal-web-app/.env')
BACKEND_URL = os.getenv("BACKEND_URL")

def upload_page():
    st.header("Upload File")
    uploaded_file = st.file_uploader("Upload file EXE untuk dianalisis", type=["exe"])
    if uploaded_file is not None:
        with st.spinner("Uploading to backend..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/octet-stream")}
            try:
                response = requests.post(f"{BACKEND_URL}/file-upload", files=files)
            except Exception as e:
                st.error(f"Gagal mengirim file: {e}")
                return  

        if response.status_code == 200:
            task_id = response.json().get("task_id")
            st.success(f"File dikirim. Task ID: {task_id}")
        else:
            try:
                error_detail = response.json().get("error", "Tidak ada detail error")
            except Exception as e:
                error_detail = f"Gagal parse error response: {e}"
            st.error(f"Upload gagal (Status {response.status_code}): {error_detail}")
            st.code(response.text, language="json")