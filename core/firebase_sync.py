import requests
import json
from datetime import datetime

class FirebaseSync:
    def __init__(self, database_url):
        self.database_url = database_url.rstrip('/')

    def sync_alert(self, alert):
        if not self.database_url:
            return
        
        try:
            # We use the REST API to avoid heavy dependencies
            # This pushes the alert to the 'alerts' node
            url = f"{self.database_url}/alerts.json"
            response = requests.post(url, json=alert)
            return response.status_code == 200
        except Exception as e:
            print(f"[!] Firebase Sync Error: {e}")
            return False

    def sync_status(self, status_info):
        if not self.database_url:
            return
            
        try:
            url = f"{self.database_url}/status.json"
            requests.put(url, json=status_info)
        except:
            pass
