import streamlit as st
from dotenv import load_dotenv
import os
import requests

load_dotenv(dotenv_path="/Users/jezzen145/sysmal-web-app/.env", override=True)
BACKEND_URL = os.getenv("BACKEND_URL")


def task_page():
    st.header("Task Status")
    st.write("Check analysis status from CAPEv2.")

    if st.button("🔄 Refresh Task List"):
        st.rerun()
    
    try:
        response = requests.get(f"{BACKEND_URL}/task-list")
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        st.error(f"Failed getting task data: {e}")
        return
    
    task_id = response.json().get("id")
    try :
        prediction_response = requests.get(f"{BACKEND_URL}/predict/{task_id}")
        prediction_response.raise_for_status()
        prediction_data = prediction_response.json()
    except Exception as e:
        st.error(f"Failed getting prediction data: {e}")
        return
    
    predict = prediction_data.get("label", "")
    tasks = data.get("tasks", [])
    print(tasks)
    if not tasks:
        st.info("There is no task")
        return
    
    st.subheader("Task List")
    rows = [
        {
            "ID": task["id"],
            "Kategori": task["category"],
            "File": task["target"],
            "Status": task["status"],
            "Prediction": predict if task["id"] == task_id else "N/A"
        }
        for task in tasks
    ]

    st.table(rows)


