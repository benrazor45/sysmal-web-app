import streamlit as st
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='/Users/jezzen145/sysmal-web-app/.env', override=True)
BACKEND_URL = os.getenv("BACKEND_URL")


def build_top_ngrams_table(ngrams):
    table_html = '<table style="margin: 0 auto; border-collapse: collapse;">'
    table_html += '<tr><th style="border: 1px solid white; padding: 8px;">N-gram</th><th style="border: 1px solid white; padding: 8px;">Score</th></tr>'
    for ngram, score in ngrams:
        table_html += f'<tr><td style="border: 1px solid white; padding: 8px;">{ngram}</td><td style="border: 1px solid white; padding: 8px;">{score:.4f}</td></tr>'
    table_html += '</table>'
    return table_html

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

        try :
            file_view_response = requests.get(f"{BACKEND_URL}/file-view/{task_id}")
            file_view_data = file_view_response.json().get("result_view", [{}])[0]
            target = file_view_data.get("target", "N/A")
            added_on = file_view_data.get("added_on", "N/A")
            file_type = file_view_data.get("file_type", "N/A")
        except Exception as e:
            target = added_on = file_type = "N/A"
            st.error(f"Failed to retrieve file view: {e}")
            return
        
        label = result["label"]
        confidence = result["confidence"]
        top_ngrams = result.get("top_ngrams", [])

        top_ngrams_html = build_top_ngrams_table(top_ngrams) if top_ngrams else "<p>No N-grams found</p>"
    
        # Display the result in a card-like format
        st.toast("Prediction completed! 🎉", icon="✅")
        card_color = "#FF4B4B" if label == "malware" else "#4CAF50"
        emoji = "🛑" if label == "malware" else "✅"

        st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display:flex; justify-content:center; align-items:center; height:80vh;">
            <div style="width:600px; background-color:{card_color}; 
                        padding:30px; border-radius:20px; box-shadow:4px 4px 20px rgba(0,0,0,0.3); 
                        color:white; text-align:center;">
                <h2 style="margin-top:0;">{emoji} Deteksi File</h2>
                <p style="font-size:18px;"><strong>Label:</strong> {label.upper()}</p>
                <p style="font-size:18px;"><strong>Confidence:</strong> {confidence:.2f}%</p>
                <hr style="border-top:1px solid #ffffff33;">
                <p style="font-size:16px;"><strong>File Name:</strong> {target}</p>
                <p style="font-size:16px;"><strong>Uploaded On:</strong> {added_on}</p>
                <p style="font-size:16px;"><strong>File Type:</strong> {file_type}</p>
                <p style="font-size:16px;"><strong>Top N-grams:</strong></p>
                {top_ngrams_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

