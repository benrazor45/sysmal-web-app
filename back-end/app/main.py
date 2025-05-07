import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
import shutil
from cape_api import submit_file, polling_status_task, get_file_reports, get_task_list
from models import extract_sequence_from_dict
from utils import save_sequence_to_csv
from dotenv import load_dotenv


app = FastAPI()

load_dotenv(dotenv_path='C:/Users/USER/sysmal-web-app/.env')
token_cape = os.getenv("TOKEN")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
LIMIT_TASK = 5
UPLOAD_FOLDER = "./uploads"
TIMEOUT = 120
INTERVAL = 5
CSV_PATH = "back-end/app/seq_csv"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/file-upload")
async def upload_file(file :UploadFile =File(...)):
    if not file.filename.endswith((".exe",)):
        raise HTTPException(status_code=400, detail="Only .exe files allowed")
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    print(file_path)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    cape_response = submit_file(file_path, token_cape)

    if "error" in cape_response and cape_response["error"]:
        return JSONResponse(status_code=500, content={"error": cape_response["error"]})
    try:
        task_id = cape_response["data"]["task_ids"][0]
        return {"task_id": task_id}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Invalid CAPEv2 response: {str(e)}"})
    
@app.get("/task-list")
def retrieve_task_list() :
    try :
        result = get_task_list(token=token_cape, limit=LIMIT_TASK)
        print("[DEBUG] Raw task list:", result)
        tasks = result.get("data", [])
        print("[DEBUG] Array task list:", tasks)
        filtered_tasks = [
            {
                "id": task.get("id"),
                "category": task.get("category"),
                "target": task.get("target"),
                "status": task.get("status")
            }
            for task in tasks
        ]
        return {"tasks": filtered_tasks}
    except Exception as e :
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tasks: {e}")

@app.get("/predict/{task_id}")
def predict_files(task_id):
    
    try :

        polling_status_task(task_id, token=token_cape, interval=INTERVAL, timeout=TIMEOUT)

        report = get_file_reports(task_id, token=token_cape)

        sequence = extract_sequence_from_dict(report)

        save_sequence_to_csv(sequence, output_csv_path=CSV_PATH, task_id=task_id)
    
    except Exception as e:
        print(f"Failed Predict Malware")












# model = load_model("model/bi_lstm_batch_64.h5")




