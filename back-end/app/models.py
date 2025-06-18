from utils import clean_api
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import pandas as pd

#Extract sequences from reports
def extract_sequence_from_dict(report_json: dict) -> str:

    if 'behavior' not in report_json or 'processes' not in report_json['behavior']:
        raise ValueError("Invalid report format: 'behavior' or 'processes' key not found.")
    
    api_calls_with_duplicates = []
    for process in report_json['behavior']['processes']:
        if 'calls' in process:
            for call in process['calls']:
                api_name = call.get('api')
                if api_name:
                    api_name = api_name.replace('_', '')
                    api_calls_with_duplicates.append(api_name)
    
    if not api_calls_with_duplicates:
        raise ValueError("No API calls found in the report.")
    
    unique_api_calls = []
    seen_apis = set()
    for api in api_calls_with_duplicates:
        if api not in seen_apis:
            unique_api_calls.append(api)
            seen_apis.add(api)

    return ' '.join(unique_api_calls)

#TF-IDF Processing
# def get_top_ngrams(sequence, ngram_range=(2,3), top_n=5):
#     tfidf = TfidfVectorizer(ngram_range=ngram_range)
#     X = tfidf.fit_transform([sequence])
#     tfidf_scores = zip(tfidf.get_feature_names_out(), X.toarray()[0])
#     sorted_scores = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)
    
#     # Kembalikan skor dan n-gram
#     # top_ngrams = [{"ngram": ngram, "score": round(score, 5)} for ngram, score in sorted_scores[:top_n]]
#     return sorted_scores[:top_n]
def generate_explanation(
    new_sequence: str, 
    prediction: str, 
    confidence_score: float, 
    malware_patterns: set, 
    benign_patterns: set
) -> str:
    """
    Menghasilkan penjelasan dinamis dengan membandingkan n-gram dari sekuens baru
    dengan pola-pola kunci yang sudah dimuat.

    Args:
        new_sequence (str): Sekuens API calls dari file yang diunggah.
        prediction (str): Hasil prediksi dari model ('malware' atau 'benign').
        confidence_score (float): Skor kepercayaan dari model dalam bentuk float (misal, 0.95).
        malware_patterns (set): Set pola n-gram malware yang sudah dimuat.
        benign_patterns (set): Set pola n-gram benign yang sudah dimuat.

    Returns:
        str: String penjelasan yang sudah diformat untuk ditampilkan di frontend.
    """
    try:
        vectorizer = CountVectorizer(ngram_range=(2, 3)).fit([new_sequence])
        new_ngrams = set(vectorizer.get_feature_names_out())
    except ValueError:
        new_ngrams = set()

    explanation = f"Hasil Prediksi: **{prediction.capitalize()}** (Tingkat Kepercayaan: {confidence_score:.2%})\n\n"
    
    if prediction.lower() == "malware":
        matched_patterns = new_ngrams.intersection(malware_patterns)
        if matched_patterns:
            explanation += "Alasan: File ini diklasifikasikan sebagai **Malware** karena mengandung pola-pola aktivitas yang sangat umum ditemukan pada perangkat lunak berbahaya, seperti:\n"
            for pattern in sorted(list(matched_patterns))[:5]: # Tampilkan maks 5 pola
                explanation += f"- `{pattern}`\n"
        else:
            explanation += "Alasan: File ini menunjukkan pola aktivitas yang konsisten dengan perilaku berbahaya, meskipun tidak cocok dengan pola malware yang paling umum."
            
    else: 
        matched_patterns = new_ngrams.intersection(benign_patterns)
        if matched_patterns:
            explanation += "Alasan: File ini diklasifikasikan sebagai **Benign** karena pola aktivitasnya konsisten dengan perangkat lunak yang aman dan umum, seperti:\n"
            for pattern in sorted(list(matched_patterns))[:5]:
                explanation += f"- `{pattern}`\n"
        else:
             explanation += "Alasan: Pola aktivitas file ini tidak menunjukkan indikator berbahaya yang signifikan."

    return explanation
