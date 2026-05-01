import requests
import json
from datetime import datetime

class CloudSync:
    def __init__(self, bucket_url):
        # Using a public anonymous KV store for instant live demo
        self.bucket_url = bucket_url.rstrip('/')

    def sync_alert(self, alert):
        if not self.bucket_url:
            return
        
        try:
            # We fetch existing alerts, append, and save back
            # (Note: For high traffic we'd use a proper DB, but for a demo this is instant)
            get_resp = requests.get(f"{self.bucket_url}/alerts")
            alerts = []
            if get_resp.status_code == 200:
                alerts = get_resp.json()
            
            alerts.append(alert)
            # Keep only last 50 alerts to stay within limits
            alerts = alerts[-50:]
            
            requests.put(f"{self.bucket_url}/alerts", json=alerts)
        except Exception as e:
            pass
