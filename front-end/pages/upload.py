import streamlit as st
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='/Users/jezzen145/sysmal-web-app/.env', override=True)
BACKEND_URL = os.getenv("BACKEND_URL")

def format_explanation_with_table(explanation_str: str) -> str:

    prose_part = []
    ngrams = []
    
    for line in explanation_str.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.startswith('- `'):
            ngram = line.replace('- `', '').replace('`', '')
            ngrams.append(ngram)
        else:
            prose_part.append(line.replace('**', '<strong>').replace('**', '</strong>'))

    html_output = "<br>".join(prose_part)

    if ngrams:
        table_style = "width: 100%; margin-top: 15px; border-collapse: collapse; background-color: rgba(255, 255, 255, 0.1);"
        th_style = "border-bottom: 2px solid rgba(255, 255, 255, 0.5); padding: 10px; text-align: center;"
        td_style = "padding: 8px 10px; border-top: 1px solid rgba(255, 255, 255, 0.2);"
        
        table_html = f'<table style="{table_style}">'
        table_html += f'<thead><tr><th style="{th_style}">Behavior Patterns</th></tr></thead>'
        table_html += '<tbody>'
        for ngram in ngrams:
            table_html += f'<tr><td style="{td_style}"><code>{ngram}</code></td></tr>'
        table_html += '</tbody></table>'
        
        html_output += table_html

    return f'<div style="text-align:center; font-family: \'Source Sans Pro\', sans-serif; white-space: normal;">{html_output}</div>'

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
        
        task_id = response.json().get("task_id")
        st.success(f"File successfully uploaded. Task ID: {task_id}")


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
            progress_bar.progress(100, text="Analyze failed ❗")

            error_detail = prediction_response.json().get("error", "")
            if "x64" in error_detail.lower():
                st.warning("File can't be analyzed (x64 is not supported by CAPEv2 Sandbox)❗")
            elif "Sequence null" in prediction_response.text:
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
        
        label = result.get("label", "N/A")
        confidence = result.get("confidence", "N/A")
        # top_ngrams = result.get("top_ngrams", [])
        explanation_raw = result.get("explanation", "No explanation provided.")

        explanation_html = format_explanation_with_table(explanation_raw)
    
        # Display the result in a card-like format
        st.toast("Prediction completed! 🎉", icon="✅")
        card_color = "#FF4B4B" if label == "Dangerous/Malware" else "#4CAF50"
        emoji = "🛑" if label == "Dangerous/Malware" else "✅"
        st.markdown(f"""
            <div style="display:flex; justify-content:center; align-items:center; height:80vh;">
                <div style="width:650px; background-color:{card_color}; 
                            padding:30px; border-radius:20px; box-shadow:4px 4px 20px rgba(0,0,0,0.3); 
                            color:white; text-align:center;">
                    <h2 style="margin-top:0;">{emoji}File Analysis Result</h2>
                    <p style="font-size:18px;">
                        <strong>Prediction:</strong> {label.upper()}
                    </p>
                    <p style="font-size:18px;">
                        <strong>
                            <span title="How confident the system is in this prediction result (the higher, the more certain).">
                                Confidence Score:
                            </span>
                        </strong>{confidence} sure
                    </p>
                    <hr style="border-top:1px solid #ffffff33;">
                    <p style="font-size:16px;"><strong>File Name:</strong> {target}</p>
                    <p style="font-size:16px;"><strong>Uploaded On:</strong> {added_on}</p>
                    <p style="font-size:16px;"><strong>File Type:</strong> {file_type}</p>
                    <p style="font-size:16px;">
                        <strong>
                            <span title="Program behavior patterns based on logged activity, such as file, network, or memory access.">
                                Common Behavior Patterns:
                            </span>
                        </strong>
                    </p>
                    <div style="text-align:center;">
                        <pre style="white-space: pre-wrap;">{explanation_html}</pre>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)


        

