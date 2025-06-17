import streamlit as st

def home_page():
    st.header("🦠Welcome to SYSMAL web app.")
    st.markdown ("""
<div style='text-align: justify; font-size: 16px; padding: 20px;'>

**SYSMAL (System Malware Analyzer)** is a web application that allows users to upload executable files (.exe) to be analyzed and predicted whether they contain malware or not.

The analysis process is carried out through framework integration **CAPEv2** to perform dynamic analysis and **model deep learning LSTM** for malware prediction based on extracted data.

This project's model repository can be found at https://github.com/benrazor45/sysmal.git

### 🔧 Key Features:
- Upload `.exe` files directly via the web interface
- Analysis process using CAPEv2 framework
- Prediction using a trained LSTM models
- View analysis status and prediction results in real-time

</div>
""", unsafe_allow_html=True)
    st.markdown("If you're not sure what ransomware is or how this app works, feel free to check out the Help page below.")
    if st.button("❓ Help"):
        st.switch_page("pages/help.py")
