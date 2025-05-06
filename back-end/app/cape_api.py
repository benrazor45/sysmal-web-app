import requests
import os
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from fastapi import HTTPException


load_dotenv(dotenv_path='C:/Users/USER/sysmal-web-app/.env')
CAPE_BASE_URL = os.getenv("CAPE_URL")
VM_NAME = "cape"
ALLOWED_EXTENSION = "exe"
LIMIT_TASK = 5

def get_task_list(token):
    url = f'{CAPE_BASE_URL}/apiv2/tasks/list/{LIMIT_TASK}'
    headers = {
        'Authorization' : f'Token {token}'
    }

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

def get_analysis_status(task_id, token):
    url = f'{CAPE_BASE_URL}/apiv2/tasks/status/{task_id}'
    headers = {
        'Authorization' : f'Token {token}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200 :
        error_msg = print("error get analysis staus")
        return error_msg
        
    return response.json()['task']['status']


def get_file_reports(task_id, token):
    url = f'{CAPE_BASE_URL}/apiv2/tasks/get/report/{task_id}/{ALLOWED_EXTENSION}'
    headers = {
        'Authorization' : f'Token {token}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        error_msg = print("error getting file reports")
        return error_msg
    
    return response.json()

# def analyze_files(file_path, token, max_wait=60):

#     submit_response = submit_file(file_path, token)
#     task_id = 

