from utils import clean_api

#Extract sequences from reports
def extract_sequence_from_dict(report_json: dict) -> str:

    resolved_apis = report_json.get('behavior', {}).get('summary', {}).get('resolved_apis', [])
    
    if not resolved_apis or not isinstance(resolved_apis, list):
        raise ValueError("Resolved apis is null or not valid.")

    cleaned = [clean_api(api) for api in resolved_apis]

    result = []
    prev = ''
    count = 0
    for api in cleaned:
        if api == prev:
            count += 1
        else:
            count = 1
        if count <= 2:
            result.append(api)
        prev = api

    return ' '.join(result)
