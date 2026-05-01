import psutil
from .logger import logger
from .detection_engine import DetectionEngine

class ServiceAudit:
    def __init__(self):
        self.engine = DetectionEngine()
        self.seen_services = set()

    def scan(self):
        current_services = []
        for service in psutil.win_service_iter():
            try:
                info = service.as_dict()
                # Try to get binpath if possible (psutil doesn't always provide it easily)
                # We can approximate or use more advanced methods if needed
                service_info = {
                    "name": info.get('name', 'Unknown'),
                    "display_name": info.get('display_name', 'Unknown'),
                    "status": info.get('status', 'Unknown'),
                    "binpath": info.get('binpath', 'Unknown'), # Some versions of psutil might not have this
                    "start_type": info.get('start_type', 'Unknown'),
                    "username": info.get('username', 'Unknown')
                }
                current_services.append(service_info)
                
                if service_info['name'] not in self.seen_services:
                    self.seen_services.add(service_info['name'])
                    alerts = self.engine.check_service(service_info)
                    for severity, reason in alerts:
                        logger.log_alert(severity, reason, {"service_name": service_info['name']})
            except Exception as e:
                continue
                
        return current_services
