import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from tensorflow.keras.models import load_model
import shutil
from cape_api import submit_file, get_analysis_status, get_file_reports
from dotenv import load_dotenv


app = FastAPI()

load_dotenv(dotenv_path='.env')

token_cape = os.getenv('TOKEN')

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

model = load_model("model/bi_lstm_batch_64.h5")




