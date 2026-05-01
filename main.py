import sys
import time
import threading
import argparse
from core.logger import logger
from core.process_monitor import ProcessMonitor
from core.service_audit import ServiceAudit
from core.reporter import SecurityReporter
from ui.cli import CLIDashboard
from ui.gui import GUIDashboard
from ui.web_server import WebDashboard

class SecurityAgent:
    def __init__(self):
        self.logger = logger
        self.proc_monitor = ProcessMonitor()
        self.service_audit = ServiceAudit()
        self.reporter = SecurityReporter()
        self.last_processes = []
        self.is_running = True

    def monitoring_loop(self):
        print("[*] Starting security monitoring loop...")
        while self.is_running:
            try:
                # 1. Scan Processes
                self.last_processes = self.proc_monitor.scan()
                
                # 2. Scan Services
                self.service_audit.scan()
                
                # Wait for next cycle
                time.sleep(10)
            except KeyboardInterrupt:
                self.is_running = False
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(10)

def main():
    parser = argparse.ArgumentParser(description="Windows Security & Process Monitoring Agent")
    parser.add_argument('--mode', choices=['cli', 'gui', 'web', 'all'], default='cli', help="Interface mode")
    args = parser.parse_args()

    agent = SecurityAgent()
    
    # Start monitoring in a background thread
    monitor_thread = threading.Thread(target=agent.monitoring_loop, daemon=True)
    monitor_thread.start()

    if args.mode == 'web' or args.mode == 'all':
        if args.mode == 'web':
            agent.logger.disable_console()
        web = WebDashboard(agent)
        web.run(port=5000)

    if args.mode == 'gui':
        gui = GUIDashboard(agent)
        gui.run()
    elif args.mode == 'all':
        print("[*] Web and GUI modes active.")
        gui = GUIDashboard(agent)
        gui.run()
    elif args.mode == 'web':
        try:
            print("[*] Web server mode only. Alerts will be shown in the web dashboard.")
            print("[*] Press Ctrl+C to exit.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] Shutting down...")
    else: # CLI mode
        cli = CLIDashboard(agent)
        try:
            cli.run()
        except KeyboardInterrupt:
            print("\n[*] Shutting down...")

if __name__ == "__main__":
    main()
