import streamlit as st
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='C:/Users/USER/sysmal-web-app/.env')
BACKEND_URL = os.getenv("BACKEND_URL")

def upload_page():
    st.header("Upload File")
    uploaded_file = st.file_uploader("Please upload an .EXE file.", type=["exe"])
    if uploaded_file is not None:
        with st.spinner("Uploading to backend..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/octet-stream")}
            try:
                response = requests.post(f"{BACKEND_URL}/file-upload", files=files)
            except Exception as e:
                st.error(f"Failed uploading file: {e}")
                return  

        if response.status_code != 200:
            try:
                error_detail = response.json().get("error", "No error detailed")
            except Exception as e:
                error_detail = f"Failed to parse error message: {e}"
            st.error(f"Upload failed (Status {response.status_code}): {error_detail}")
            st.code(response.text, language="json")
            return

        # if response.status_code == 200:
        #     task_id = response.json().get("task_id")
        #     st.success(f"File dikirim. Task ID: {task_id}")
        
        
        task_id = response.json().get("task_id")
        st.success(f"File successfully uploaded. Task ID: {task_id}")


        # progress_bar = st.progress(0, text="Menunggu CAPEv2 selesai menganalisis...")
        # progress_val = 0
    
        # while progress_val < 70: 
        #     time.sleep(3)
        #     progress_val += 10
        #     progress_bar.progress(progress_val, text=f"Menganalisis file... {progress_val}%")
        
        # try:
        #     prediction_response = requests.get(f"{BACKEND_URL}/predict/{task_id}")
        # except Exception as e:
        #     st.error(f"Gagal mendapatkan prediksi: {e}")
        #     return


        progress_bar = st.progress(0, text="Waiting CAPEv2 analyze the file...")
        for progress_val in range(0, 71, 10):
            time.sleep(3)
            progress_bar.progress(progress_val, text=f"Analyzing the file... {progress_val}%")

        try:
            prediction_response = requests.get(f"{BACKEND_URL}/predict/{task_id}")
        except Exception as e:
            st.error(f"Failed getting prediction: {e}")
            return
        
        if prediction_response.status_code != 200:
            progress_bar.progress(100, text="Analyze complete without prediction result ❗")

            if "Sequence null" in prediction_response.text:
                st.warning("File can't be predicted (resolved_apis is null)")
            else:
                st.error("Prediction failed.")
                st.code(prediction_response.text, language="json")
            return
        
        progress_bar.progress(100, text="Analyzing and Prediction completed ✅")
        result = prediction_response.json()
        label = result["label"]
        confidence = result["confidence"]

        st.toast("Prediction completed! 🎉", icon="✅")
        card_color = "#FF4B4B" if label == "malware" else "#4CAF50"
        emoji = "🛑" if label == "malware" else "✅"

        st.markdown(f"""
        <div style="position:fixed; bottom:20px; right:20px; width:300px; background-color:{card_color}; 
                    padding:20px; border-radius:10px; box-shadow:2px 2px 10px rgba(0,0,0,0.3); color:white;">
            <h4 style="margin-top:0;">{emoji} Deteksi File</h4>
            <p><strong>Label:</strong> {label.upper()}</p>
            <p><strong>Confidence:</strong> {confidence:.2f}</p>
        </div>
        """, unsafe_allow_html=True)

