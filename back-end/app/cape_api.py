import requests
import time
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import HTTPException


load_dotenv(dotenv_path='C:/Users/USER/sysmal-web-app/.env')
CAPE_BASE_URL = os.getenv("CAPE_URL")
VM_NAME = "cape"
ALLOWED_EXTENSION = "exe"

#Upload File
def get_task_list(token, limit):
    url = f'{CAPE_BASE_URL}/apiv2/tasks/list/{limit}'
    headers = {
        'Authorization' : f'Token {token}'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Gagal mengambil daftar task: {e}")
        raise HTTPException(status_code=500, detail=f"Gagal ambil task list: {e}")

    
#Upload File
def submit_file(file_path, token):
    url = f'{CAPE_BASE_URL}/apiv2/tasks/create/file/'
    headers = {
        'Authorization' : f'Token {token}'
    }
    files = {'file': open(file_path, 'rb')}
    # data = {'package' : 'exe'}

    try:
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Gagal mengirim ke CAPEv2: {e}")
        raise HTTPException(status_code=500, detail=f"Gagal submit ke CAPEv2: {e}")


#Polling Task    
def polling_status_task(task_id, token, interval, timeout):
    url = f'{CAPE_BASE_URL}/apiv2/tasks/status/{task_id}'
    headers = {
        'Authorization' : f'Token {token}'
    }
    start = time.time()
    while True :
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        status = data.get("task", {}).get("status", "")
        if status.lower() == "reported":
            return True
        
        if time.time() - start > timeout:
            raise TimeoutError(f"Task {task_id} belum selesai dalam {timeout} detik.")
        
        time.sleep(interval)

#Get File Reports
def get_file_reports(task_id, token):
    url = f'{CAPE_BASE_URL}/apiv2/tasks/get/report/{task_id}'
    headers = {
        'Authorization' : f'Token {token}'
    }
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Gagal mengirim ke CAPEv2: {e}")
        raise HTTPException(status_code=500, detail=f"Gagal submit ke CAPEv2: {e}")

# def analyze_files(file_path, token, max_wait=60):

#     submit_response = submit_file(file_path, token)
#     task_id = 

