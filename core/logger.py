import logging
import json
import os
from datetime import datetime

class AgentLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        self.log_file = os.path.join(self.log_dir, "agent.log")
        self.alerts_file = os.path.join(self.log_dir, "alerts.json")
        
        # Set up standard logging
        self.file_handler = logging.FileHandler(self.log_file)
        self.stream_handler = logging.StreamHandler()
        self.formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        
        self.file_handler.setFormatter(self.formatter)
        self.stream_handler.setFormatter(self.formatter)
        
        self.logger = logging.getLogger("SecurityAgent")
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)
        
        # Initialize alerts file if not exists
        if not os.path.exists(self.alerts_file):
            with open(self.alerts_file, 'w') as f:
                json.dump([], f)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def log_alert(self, severity, reason, process_info):
        alert = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "severity": severity,
            "reason": reason,
            "process": process_info
        }
        
        self.logger.warning(f"ALERT [{severity}] {reason} - {process_info.get('name', 'Unknown')}")
        
        try:
            with open(self.alerts_file, 'r+') as f:
                data = json.load(f)
                data.append(alert)
                f.seek(0)
                json.dump(data, f, indent=4)
        except Exception as e:
            self.logger.error(f"Failed to log alert to JSON: {e}")

    def get_alerts(self):
        try:
            with open(self.alerts_file, 'r') as f:
                return json.load(f)
        except:
            return []

    def disable_console(self):
        self.logger.removeHandler(self.stream_handler)

# Singleton instance
logger = AgentLogger()
