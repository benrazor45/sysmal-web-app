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

#Get task list
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
        print(f"[ERROR] Failed getting task list : {e}")
        raise HTTPException(status_code=500, detail=f"Failed getting task list: {e}")

    
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
        print(f"[ERROR] Failed upload to CAPEv2: {e}")
        raise HTTPException(status_code=500, detail=f"Failed submit to CAPEv2: {e}")


#Polling Task    
def polling_status_task(task_id, token, interval, timeout, retry):
    url = f'{CAPE_BASE_URL}/apiv2/tasks/status/{task_id}'
    headers = {
        'Authorization' : f'Token {token}'
    }
    start = time.time()
    retry_count = 0
    while True :
        try :
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            status = data.get("data", "")
            if status == "reported":
                print(f"[INFO] Task {task_id} sucessfully processed.")
                return True
            
            elif status == "pending":
                print(f"[INFO] Task {task_id} still pending...")
            
            else:
                print(f"[INFO] Task {task_id} status: {status}")

            
            retry_count = 0
        
        except requests.RequestException as e:
            print(f"[WARN] Failed getting task status {task_id}, retry {retry_count + 1}/{retry}: {e}")
            retry_count += 1
            if retry_count >= retry:
                raise Exception(f"Task {task_id} failed to processed after {retry} attempts.")
        

        elapsed = time.time() - start
        if elapsed > timeout:
            raise Exception(f"Task {task_id} is not done in {timeout} seconds.")

        time.sleep(interval)

#Get File Reports
def get_file_reports(task_id, token, retry, delay):
    url = f'{CAPE_BASE_URL}/apiv2/tasks/get/report/{task_id}'
    headers = {
        'Authorization' : f'Token {token}'
    }
    for attempt in range(retry) : 
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            print (response)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[WARN] Failed getting task report {task_id} (attempt {attempt + 1}/{retry}): {e}")
            time.sleep(delay)

    raise Exception(f"Failed getting report from CAPEv2 after {retry} attempts.")

# def analyze_files(file_path, token, max_wait=60):

#     submit_response = submit_file(file_path, token)
#     task_id = 

