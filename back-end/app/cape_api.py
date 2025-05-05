import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')
CAPE_BASE_URL = os.getenv('CAPE_API_URL')
ALLOWED_EXTENSION = "exe"

def submit_file(file_path, token):
    url = f'{CAPE_BASE_URL}/apiv2/tasks/create/file/'
    headers = {
        'Authorization' : f'{token}'
    }
    files = {'files': open(file_path, 'rb')}
    data = {'package' : 'exe'}
    response = requests.post(url, headers=headers, files=files, data=data)
    return response.json()

def get_analysis_status(task_id, token):
    url = f'{CAPE_BASE_URL}/apiv2/tasks/status/{task_id}'
    headers = {
        'Authorization' : f'{token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()['task']['status']

def get_file_reports(task_id, token):
    url = f'{CAPE_BASE_URL}/apiv2/tasks/get/report/{task_id}/{ALLOWED_EXTENSION}'
    headers = {
        'Authorization' : f'{token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

