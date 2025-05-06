import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
import shutil
from cape_api import submit_file, get_analysis_status, get_file_reports
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

UPLOAD_FOLDER = "./uploads"
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


# model = load_model("model/bi_lstm_batch_64.h5")




