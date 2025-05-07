import pandas as pd
import os

#Cleaning API
def clean_api(api: str) -> str:
    
    if '.' in api:
        return api.split('.')[-1]
    return api

#Save sequences to csv
def save_sequence_to_csv(sequence: str, output_csv_path: str, task_id):

    os.makedirs(output_csv_path, exist_ok=True)
    csv_path = os.path.join(output_csv_path, f'{task_id}.csv')
    df = pd.DataFrame([{'sequence': sequence}])
    df.to_csv(csv_path, index=False)