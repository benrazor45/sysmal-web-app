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

def generate_explanation(
    new_sequence: str, 
    prediction: str, 
    confidence_score: float, 
    malware_patterns: set, 
    benign_patterns: set
) -> str:

    try:
        vectorizer = CountVectorizer(ngram_range=(2, 3)).fit([new_sequence])
        new_ngrams = set(vectorizer.get_feature_names_out())
    except ValueError:
        new_ngrams = set()

    explanation = f""
    
    if prediction == "Dangerous/Malware":
        matched_patterns = new_ngrams.intersection(malware_patterns)
        if matched_patterns:
            explanation += "This file is classified as **Malware** because it contains activity patterns that are very common in malicious software, such as:\n"
            for pattern in sorted(list(matched_patterns))[:5]: # Tampilkan maks 5 pola
                explanation += f"- `{pattern}`\n"
        else:
            explanation += "This file shows a pattern of activity consistent with malicious behavior, although it does not match the most common malware patterns."
            
    else: 
        matched_patterns = new_ngrams.intersection(benign_patterns)
        if matched_patterns:
            explanation += "This file is classified as **Benign** because its activity pattern is consistent with that of safe, common software, such as:\n"
            for pattern in sorted(list(matched_patterns))[:5]:
                explanation += f"- `{pattern}`\n"
        else:
             explanation += "This file's activity pattern does not show any significant malicious indicators."

    return explanation
