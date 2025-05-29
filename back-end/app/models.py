from utils import clean_api
from sklearn.feature_extraction.text import TfidfVectorizer
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
def get_top_ngrams(sequence, ngram_range=(2,3), top_n=5):
    tfidf = TfidfVectorizer(ngram_range=ngram_range)
    X = tfidf.fit_transform([sequence])
    tfidf_scores = zip(tfidf.get_feature_names_out(), X.toarray()[0])
    sorted_scores = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)
    top_ngrams = [ngram for ngram, score in sorted_scores[:top_n]]
    return top_ngrams
