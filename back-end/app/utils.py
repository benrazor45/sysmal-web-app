import pandas as pd
import os
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences


#Cleaning API
def clean_api(api: str) -> str:
    
    if '_' in api:
        return api.split('.')[-1]
    return api

#Save sequences to csv
def save_sequence_to_csv(sequence, output_csv_path, task_id):

    try : 
        # os.makedirs(output_csv_path, exist_ok=True)
        csv_path = os.path.join(output_csv_path, f'{task_id}.csv')
        df = pd.DataFrame([{'sequence': sequence}])
        df.to_csv(csv_path, index=False)
        print(f"[INFO] Sequenced CSV saved in: {csv_path}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed save sequence to CSV: {e}")
        return False

def read_sequence_from_csv(csv_folder, task_id):
    csv_path = os.path.join(csv_folder, f'{task_id}.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File {task_id}.csv not found")
    
    df = pd.read_csv(csv_path)
    if 'sequence' not in df.columns:
        raise ValueError("CSV file does not contain 'sequence' column")
    
    sequence_text = df['sequence'].iloc[0]
    return sequence_text

#Tokenization
def tokenization(task_id, csv_folder):

    with open('./tokenizer/tokenizer_new.pkl', 'rb') as f:
        tokenizer = pickle.load(f)

    with open('./tokenizer/maxlen_new.txt', 'r') as f:
        maxlen = int(f.read())
    
    csv_path = os.path.join(csv_folder, f'{task_id}.csv')
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File {task_id}.csv not found")

    df = pd.read_csv(csv_path)
    sequence_text =  df['sequence'].iloc[0]

    sequence = tokenizer.texts_to_sequences([sequence_text])
    padded_sequence = pad_sequences(sequence, padding='post', truncating='post', maxlen=maxlen)

    return padded_sequence



