import psutil
import time
from .logger import logger
from .detection_engine import DetectionEngine

class ProcessMonitor:
    def __init__(self):
        self.engine = DetectionEngine()
        self.seen_pids = set()

    def get_process_info(self, proc):
        try:
            with proc.oneshot():
                return {
                    "pid": proc.pid,
                    "ppid": proc.ppid(),
                    "name": proc.name(),
                    "exe": proc.exe(),
                    "username": proc.username(),
                    "create_time": proc.create_time(),
                    "parent_name": proc.parent().name() if proc.parent() else "None"
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return None

    def scan(self):
        current_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            proc_info = self.get_process_info(proc)
            if proc_info:
                current_processes.append(proc_info)
                
                # If it's a new process, check it
                if proc.pid not in self.seen_pids:
                    self.seen_pids.add(proc.pid)
                    alerts = self.engine.check_process(proc_info)
                    for severity, reason in alerts:
                        logger.log_alert(severity, reason, proc_info)
        
        # Clean up seen_pids for processes that have exited
        current_pids = {p['pid'] for p in current_processes}
        self.seen_pids = self.seen_pids.intersection(current_pids)
        
        return current_processes
