import streamlit as st
import requests
from streamlit_option_menu import option_menu
from pages import upload, home, task


st.markdown("<h2 style='text-align: center; font-weight: bold;'>Systematic Sequential Malware Analysis </h2>", unsafe_allow_html=True)
st.markdown("<h7> </h7>", unsafe_allow_html=True)

hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

selected = option_menu(None, ["Home", "Uploads", "Task"], 
    icons=['house', 'cloud-upload', "list-task"], 
    menu_icon="cast", default_index=0, orientation="horizontal")
# selected

if selected == "Home" :
    home.home_page()

elif selected == "Uploads":
    upload.upload_page()
    
elif selected == "Task":
    task.task_page()

