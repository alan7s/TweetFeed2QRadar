# TweetFeed2QRadar
Fetches logs from https://tweetfeed.live to QRadar

Prerequisites
-------------

*   **Python**: Version 3.6 or later.
    
*  **Libraries**: `requests`, `urllib3`
    
*   **QRadar**: Active QRadar instance with API access.

Setup
-----

1.  Download the script TweetFeed2QRadar.py .
    
2.  Configure the following constants in the script:
           
    *   `QRADAR_SEC_TOKEN`: Your QRadar API security token.
        
    *   `QRADAR_URL_BASE`: Base URL of your QRadar instance.
        
    *   `REFERENCE_SET_TWEETFEED_IP`: Reference set ID used to track IPs.

    *   `REFERENCE_SET_TWEETFEED_DOMAIN`: Reference set ID used to track domains.
  
    *   `REFERENCE_SET_TWEETFEED_URL`: Reference set ID used to track URLs.
  
    *   `REFERENCE_SET_TWEETFEED_SHA256`: Reference set ID used to track SHA256 hash.
  
    *   `REFERENCE_SET_TWEETFEED_MD5`: Reference set ID used to track MD5 hash.
        
3.  Disable SSL verification warnings (optional):
* The script suppresses SSL warnings to handle self-signed certificates. If necessary, you can enable them by removing:
```python
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```
How to Use
----------

1. **Execute**
```bash
python TweetFeed2QRadar.py
```
    
2.  **What it does**:
    
    *   Fetch logs from the TweetFeed API.
    *   Check if the IoC already exists in the corresponding QRadar reference set.
    *   Add the IoC to QRadar if it doesn't already exist.

Code Overview
-------------

### Functions

1.  **fetch_logs()** Fetches logs from the TweetFeed API endpoint: https://api.tweetfeed.live/v1/today.
2.  **generate_hash(log)** Generates a unique MD5 hash for a log.
3.  **get_from_qradar(reference_set_id, log_hash)** Checks if a log's hash exists in a QRadar reference set.
4.  **send_to_qradar(log_hash, ioc, reference_set_id)** Sends an IOC to QRadar, associating it with the specified reference set.
        

Notes
-----
*   Install the script as a cron job that runs every 15 minutes on your QRadar.
```bash
chmod 755 /opt/qradar/bin/TweetFeed2QRadar.py
crontab -e
*/15 * * * * /usr/bin/python /opt/qradar/bin/TweetFeed2QRadar.py
````

*   Configure the constants correctly before running the script.
       
*   Tune your QRadar Rules with the Referece Sets you have created.
