import requests
import urllib3
import urllib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import hashlib
import json

### TweetFeed2Qradar Config ###
QRADAR_SEC_TOKEN = "YOUR_SEC_TOKEN"
QRADAR_URL_BASE = "https://YOUR_QRADAR_IP"
REFERENCE_SET_TWEETFEED_IP = 100 #Your reference set ID
REFERENCE_SET_TWEETFEED_DOMAIN = 101 #Your reference set ID
REFERENCE_SET_TWEETFEED_URL = 102 #Your reference set ID
REFERENCE_SET_TWEETFEED_SHA256 = 103 #Your reference set ID
REFERENCE_SET_TWEETFEED_MD5 = 104 #Your reference set ID
###############################

def generate_hash(log):
    log_str = json.dumps(log, sort_keys=True)
    return hashlib.md5(log_str.encode('utf-8')).hexdigest()

def get_from_qradar(reference_set_id,origin):
    query = f"collection_id={reference_set_id} and source=\"{origin}\""
    encoded_query = urllib.parse.quote(query, safe="")
    qradar_url = QRADAR_URL_BASE + '/api/reference_data_collections/set_entries?fields=value&filter=' + encoded_query
    qradar_header = {
        'SEC':QRADAR_SEC_TOKEN,
        'Content-Type':'application/json',
        'Accept':'application/json'
    }
    try:
        response = requests.get(qradar_url, headers=qradar_header, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def send_to_qradar(origin,ioc,reference_set_id):
    qradar_url = QRADAR_URL_BASE + '/api/reference_data_collections/set_entries?fields=value&filter=collection_id%3D' + str(reference_set_id)
    qradar_header = {
        'SEC':QRADAR_SEC_TOKEN,
        'Content-Type':'application/json',
        'Accept':'application/json'
    }
    data = {
        "collection_id": reference_set_id,
        "source": f"{origin}",
        "value": f"{ioc}"
    }
    try:
        response = requests.post(qradar_url, headers=qradar_header, json=data, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []
    
def fetch_logs():
    url = "https://api.tweetfeed.live/v1/today"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []

def main():
    logs = fetch_logs()
    reference_set_mapping = {
        'ip': REFERENCE_SET_TWEETFEED_IP,
        'domain': REFERENCE_SET_TWEETFEED_DOMAIN,
        'url': REFERENCE_SET_TWEETFEED_URL,
        'sha256': REFERENCE_SET_TWEETFEED_SHA256,
        'md5': REFERENCE_SET_TWEETFEED_MD5
    }

    for log in reversed(logs):
        log_type = log['type']
        log_hash = generate_hash(log)
        if log_type in reference_set_mapping:
            origin = log['tweet'] + " log_hash(" + log_hash + ")"
            reference_set = reference_set_mapping[log_type]
            if get_from_qradar(reference_set,origin):
                break           
            else:
                send_to_qradar(origin, log['value'], reference_set)

if __name__ == "__main__":
    main()
