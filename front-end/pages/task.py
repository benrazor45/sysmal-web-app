import streamlit as st
from dotenv import load_dotenv
import os
import requests
import pandas as pd
import plotly.express as px

load_dotenv(dotenv_path="/Users/jezzen145/sysmal-web-app/.env", override=True)
BACKEND_URL = os.getenv("BACKEND_URL")


def task_page():
    st.header("Task Status")
    st.write("Check analysis status from CAPEv2.")

    if st.button("🔄 Refresh Task List"):
        st.rerun()
    
    try:
        response = requests.get(f"{BACKEND_URL}/task-list-details")
        response.raise_for_status()
        tasks = response.json().get("tasks", [])

    except requests.exceptions.RequestException as e:
        st.error(f"Failed connect to backend: {e}")
        return
    except Exception as e:
        st.error(f"Failed getting task data: {e}")
        return

    if not tasks:
        st.info("Belum ada riwayat analisis untuk ditampilkan.")
        return
    
    completed_tasks = [t for t in tasks if t.get('status') in ['completed', 'reported'] and t.get('prediction') not in [None, 'Analisis...']]

    st.subheader("Summary of Completed Tasks")

    total_completed = len(completed_tasks)
    ransomware_count = sum(1 for t in completed_tasks if t.get('prediction') == 'Dangerous/Malware')

    durations = [t['duration'] for t in completed_tasks if t.get('duration') is not None]
    avg_duration = sum(durations) / len(durations) if durations else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Analisis Selesai", f"{total_completed}")
    col2.metric("File Berbahaya Terdeteksi", f"{ransomware_count}")
    col3.metric("Waktu Deteksi Rata-rata", f"{avg_duration:.3f} detik")

    st.markdown("---")

    if completed_tasks:
        st.subheader("Analysis Results Visualization")
        df_predictions = pd.DataFrame(completed_tasks)
        
        prediction_counts = df_predictions['prediction'].value_counts().reset_index()
        
        fig_pie = px.pie(prediction_counts, 
                         values='count', 
                         names='prediction', 
                         title='Analysis Distribution Results',
                         color='prediction',
                         color_discrete_map={'Dangerous/Malware':'#E74C3C', 'Safe/Benign':'#2ECC71'},
                         labels={'prediction': 'Prediction Results'})
        st.plotly_chart(fig_pie, use_container_width=True)
    
    st.markdown("---")

    st.subheader("Analysis Details")

    display_data = []
    for task in tasks:
        duration = task.get('duration')
        duration_text = f"{duration:.3f} detik" if duration is not None else "N/A"
        
        display_data.append({
            "ID": task.get("id"),
            "File Name": task.get("target"),
            "Analysis Status": task.get("status"),
            "Prediction Results": task.get("prediction", "N/A"),
            "Model Predicts Time": duration_text
        })
    
    df = pd.DataFrame(display_data)

    if not df.empty and "ID" in df.columns:
        df = df.sort_values(by="ID", ascending=False)

    def style_predictions(val):
        if val == 'Dangerous/Malware':
            color = '#E74C3C'  
        elif val == 'Safe/Benign':
            color = '#2ECC71'  
        else:
            color = 'gray'
        return f'color: {color}; font-weight: bold;'

    # Tampilkan tabel menggunakan st.dataframe untuk styling
    st.dataframe(
        df.style.apply(lambda s: s.map(style_predictions), subset=['Prediction Results']),
        use_container_width=True,
        hide_index=True
    )


