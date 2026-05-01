import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

class GUIDashboard:
    def __init__(self, agent):
        self.agent = agent
        self.root = tk.Tk()
        self.root.title("Windows Security Agent")
        self.root.geometry("800x600")
        
        self.setup_ui()
        self.update_thread = threading.Thread(target=self.refresh_data, daemon=True)
        self.update_thread.start()

    def setup_ui(self):
        # Notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill='both')
        
        # Tab 1: Dashboard
        self.dash_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.dash_frame, text="Dashboard")
        
        self.lbl_status = ttk.Label(self.dash_frame, text="Status: Monitoring Active", font=("Arial", 12, "bold"))
        self.lbl_status.pack(pady=10)
        
        # Alerts Treeview
        self.alert_tree = ttk.Treeview(self.dash_frame, columns=("Time", "Severity", "Reason"), show="headings")
        self.alert_tree.heading("Time", text="Time")
        self.alert_tree.heading("Severity", text="Severity")
        self.alert_tree.heading("Reason", text="Reason")
        self.alert_tree.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Tab 2: Processes
        self.proc_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.proc_frame, text="Processes")
        
        self.proc_tree = ttk.Treeview(self.proc_frame, columns=("PID", "Name", "User"), show="headings")
        self.proc_tree.heading("PID", text="PID")
        self.proc_tree.heading("Name", text="Name")
        self.proc_tree.heading("User", text="User")
        self.proc_tree.pack(expand=True, fill='both', padx=10, pady=5)
        
        # Buttons
        self.btn_report = ttk.Button(self.root, text="Generate PDF Report", command=self.generate_report)
        self.btn_report.pack(pady=10)

    def generate_report(self):
        alerts = self.agent.logger.get_alerts()
        path = self.agent.reporter.generate_pdf_report(alerts)
        messagebox.showinfo("Report Generated", f"PDF Report saved to:\n{path}")

    def refresh_data(self):
        while True:
            # Update Alerts
            alerts = self.agent.logger.get_alerts()
            self.alert_tree.delete(*self.alert_tree.get_children())
            for alert in reversed(alerts[-20:]):
                self.alert_tree.insert("", "end", values=(alert['timestamp'], alert['severity'], alert['reason']))
            
            # Update Processes
            self.proc_tree.delete(*self.proc_tree.get_children())
            for p in self.agent.last_processes[:20]:
                self.proc_tree.insert("", "end", values=(p.get('pid'), p.get('name'), p.get('username')))
                
            time.sleep(5)

    def run(self):
        self.root.mainloop()
