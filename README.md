# TweetFeed2QRadar
Fetches logs from the tweetfeed.live to QRadar

*   Install the script as a cron job that runs every 15 minutes.
```bash
chmod 755 /opt/qradar/bin/TweetFeed2QRadar.py
crontab -e
*/15 * * * * /usr/bin/python /opt/qradar/bin/TweetFeed2QRadar.py
````
