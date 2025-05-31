import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
import shutil
from cape_api import submit_file, polling_status_task, get_file_reports, get_task_list, get_file_view
from models import extract_sequence_from_dict, get_top_ngrams
from utils import save_sequence_to_csv, tokenization, read_sequence_from_csv
from dotenv import load_dotenv


app = FastAPI()

load_dotenv(dotenv_path='/Users/jezzen145/sysmal-web-app/.env', override=True)
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
TIMEOUT = 600
INTERVAL = 5
RETRY_LIMIT = 3
DELAY = 5
CSV_PATH = "./seq_csv"
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

        polling_status_task(task_id, token=token_cape, interval=INTERVAL, timeout=TIMEOUT, retry=RETRY_LIMIT)

        report = get_file_reports(task_id, token=token_cape, retry=RETRY_LIMIT, delay=DELAY)

        sequence = extract_sequence_from_dict(report)

        if not sequence.strip():
            raise HTTPException(status_code=422, detail="Sequence null : File don't have API activities.")

        succes_save_to_csv = save_sequence_to_csv(sequence, output_csv_path=CSV_PATH, task_id=task_id)
        if not succes_save_to_csv:
            raise HTTPException(status_code=500, detail="Failed to save sequence to CSV")

        try : 
            padded_sequence = tokenization(task_id, csv_folder=CSV_PATH)
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=f"CSV file not found for task {task_id}: {str(e)}")
        except Exception as e:
            print(f"Error during tokenization: {str(e)}")

        model = load_model('./model/bi_model_batch64_5_05.h5')
        prediction = model.predict(padded_sequence)

        threshold = 0.5
        if prediction[0][0] > threshold:
            prediction_label = "malware"
            confidence = prediction[0][0] * 100
        else:
            prediction_label = "benign"
            confidence = (1 - prediction[0][0]) * 100
        
        sequence_text = read_sequence_from_csv(csv_folder=CSV_PATH, task_id=task_id)
        top_ngrams = get_top_ngrams(sequence_text)



        # label = "malware" if prediction[0][0] >= 0.5 else "benign"
        # confidence = float(prediction[0][0])

        return {
            "task_id": task_id,
            "label": prediction_label,
            "confidence": confidence,
            "top_ngrams": top_ngrams
        }
    except Exception as e:
        print(f"Failed Predict Malware")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/file-view/{task_id}")
def file_view(task_id):
    try:
        view = get_file_view(task_id, token=token_cape, retry=RETRY_LIMIT, delay=DELAY)
        target = view.get("data", {}).get("target", "")
        added_on = view.get("data", {}).get("added_on", "")
        file_type = view.get("data", {}).get("sample", {}).get("file_type", "")
        result_view = [{
            "target": target,
            "added_on": added_on,
            "file_type": file_type
        }]
        return {'result_view': result_view}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve file view: {str(e)}")










# model = load_model("model/bi_lstm_batch_64.h5")




