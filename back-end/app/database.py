# database.py

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "predictions.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    conn = get_db_connection()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS model_predictions (
        cape_task_id INTEGER PRIMARY KEY,
        prediction_result TEXT NOT NULL,
        detection_duration_seconds REAL, 
        prediction_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn.execute(create_table_query)
    conn.commit()
    conn.close()
    print("Database dengan kolom durasi berhasil disiapkan.")

def save_prediction(task_id: int, prediction: str, duration: float): # DIUBAH
    sql = """
    INSERT OR REPLACE INTO model_predictions 
    (cape_task_id, prediction_result, detection_duration_seconds)
    VALUES (?, ?, ?);
    """
    try:
        conn = get_db_connection()
        conn.execute(sql, (task_id, prediction, duration)) # DIUBAH
        conn.commit()
        print(f"Hasil untuk task_id {task_id} disimpan. Durasi: {duration:.4f} detik.")
    except sqlite3.Error as e:
        print(f"Gagal menyimpan prediksi: {e}")
    finally:
        if conn:
            conn.close()

def get_all_predictions() -> dict:
    predictions = {}
    try:
        conn = get_db_connection()
        cursor = conn.execute("SELECT cape_task_id, prediction_result, detection_duration_seconds FROM model_predictions")
        for row in cursor.fetchall():
            predictions[row['cape_task_id']] = {
                'prediction': row['prediction_result'],
                'duration': row['detection_duration_seconds']
            }
    except sqlite3.Error as e:
        print(f"Gagal mengambil data prediksi: {e}")
    finally:
        if conn:
            conn.close()
    return predictions

if __name__ == '__main__':
    setup_database()