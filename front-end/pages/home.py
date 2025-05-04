import streamlit as st

def home_page():
    st.header("🦠Welcome to SYSMAL web app.")
    st.markdown ("""
<div style='text-align: justify; font-size: 16px; padding: 20px;'>

**SYSMAL (System Malware Analyzer)** adalah web aplikasi yang memungkinkan pengguna mengunggah file executable (.exe) untuk dianalisis dan diprediksi apakah mengandung malware atau tidak.

Proses analisis dilakukan melalui integrasi framework **CAPEv2** untuk melakukan dynamic analysis dan **model deep learning LSTM** untuk prediksi malware berdasarkan data hasil ekstraksi.

Repository model project ini dapat ditemukan di https://github.com/benrazor45/sysmal.git

### 🔧 Fitur Utama:
- Upload file `.exe` secara langsung melalui antarmuka web
- Proses analisis menggunakan framework CAPEv2
- Prediksi menggunakan model LSTM yang telah dilatih
- Tampilan status analisis dan hasil prediksi secara real-time

</div>
""", unsafe_allow_html=True)
