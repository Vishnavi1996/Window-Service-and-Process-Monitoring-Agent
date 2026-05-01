import os
import difflib

class DetectionEngine:
    def __init__(self):
        # Common legitimate processes for mimicking detection
        self.legit_processes = [
            "svchost.exe", "explorer.exe", "lsass.exe", "services.exe", 
            "wininit.exe", "csrss.exe", "smss.exe", "taskhostw.exe",
            "winlogon.exe", "spoolsv.exe"
        ]
        
        # Suspicious parent-child relationships
        self.suspicious_chains = {
            "winword.exe": ["powershell.exe", "cmd.exe", "cscript.exe", "wscript.exe"],
            "excel.exe": ["powershell.exe", "cmd.exe"],
            "outlook.exe": ["powershell.exe", "cmd.exe"],
            "chrome.exe": ["cmd.exe", "powershell.exe"],
            "msedge.exe": ["cmd.exe", "powershell.exe"],
            "firefox.exe": ["cmd.exe", "powershell.exe"]
        }
        
        # Risk directories
        self.risk_dirs = [
            "temp",
            "appdata\\local\\temp",
            "downloads"
        ]
        
        self.whitelist = ["py.exe", "python.exe", "code.exe"]
        self.blacklist = ["mimikatz.exe", "nc.exe"]

    def check_process(self, proc_info):
        alerts = []
        name = proc_info.get('name', '').lower()
        path = proc_info.get('exe', '').lower()
        parent_name = proc_info.get('parent_name', '').lower()
        
        # 1. Blacklist check
        if name in self.blacklist:
            alerts.append(("CRITICAL", f"Blacklisted process detected: {name}"))
            
        # 2. Mimicking check
        for legit in self.legit_processes:
            if name != legit and difflib.SequenceMatcher(None, name, legit).ratio() > 0.8:
                alerts.append(("HIGH", f"Process name mimicking detected: {name} mimics {legit}"))
        
        # 3. Directory risk check
        for risk_dir in self.risk_dirs:
            if risk_dir in path:
                alerts.append(("MEDIUM", f"Process running from risk directory: {path}"))
                
        # 4. Suspicious chain check
        if parent_name in self.suspicious_chains:
            if name in self.suspicious_chains[parent_name]:
                alerts.append(("HIGH", f"Suspicious process chain: {parent_name} -> {name}"))
                
        # 5. Unknown/Unsigned (Simplified: not in whitelist and not in common Windows dirs)
        if name not in self.whitelist and "windows" not in path and "program files" not in path:
            if path and not any(rd in path for rd in self.risk_dirs): # If not already flagged by dir risk
                 alerts.append(("LOW", f"Unknown process running from non-standard location: {path}"))

        return alerts

    def check_service(self, service_info):
        alerts = []
        name = service_info.get('name', '').lower()
        bin_path = service_info.get('binpath', '').lower()
        
        # 1. Service in risk directory
        for risk_dir in self.risk_dirs:
            if risk_dir in bin_path:
                alerts.append(("CRITICAL", f"Service running from risk directory: {bin_path}"))
                
        # 2. Suspicious service name
        suspicious_keywords = ["hack", "crack", "miner", "keylog", "stealer"]
        if any(kw in name for kw in suspicious_keywords):
            alerts.append(("HIGH", f"Suspicious service name detected: {name}"))
            
        return alerts
