import os
import json
from datetime import datetime
from fpdf import FPDF
from .logger import logger

class SecurityReporter:
    def __init__(self, reports_dir="reports"):
        self.reports_dir = reports_dir
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

    def generate_text_report(self, alerts):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.reports_dir, f"report_{timestamp}.txt")
        
        with open(report_path, 'w') as f:
            f.write("--- WINDOWS SECURITY AGENT REPORT ---\n")
            f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Alerts: {len(alerts)}\n")
            f.write("-" * 40 + "\n\n")
            
            for alert in alerts:
                f.write(f"[{alert['severity']}] {alert['timestamp']}\n")
                f.write(f"Reason: {alert['reason']}\n")
                f.write(f"Details: {json.dumps(alert['process'], indent=2)}\n")
                f.write("-" * 20 + "\n")
                
        return report_path

    def generate_pdf_report(self, alerts):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(self.reports_dir, f"report_{timestamp}.pdf")
        
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="Windows Security Agent Report", ln=True, align="C")
        pdf.set_font("Arial", "", 10)
        pdf.cell(200, 10, txt=f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
        pdf.ln(10)
        
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt=f"Summary: {len(alerts)} alerts detected", ln=True)
        pdf.ln(5)
        
        for alert in alerts:
            pdf.set_font("Arial", "B", 10)
            color = (0, 0, 0)
            if alert['severity'] == "CRITICAL": color = (255, 0, 0)
            elif alert['severity'] == "HIGH": color = (255, 69, 0)
            elif alert['severity'] == "MEDIUM": color = (255, 165, 0)
            
            pdf.set_text_color(*color)
            pdf.cell(0, 10, txt=f"[{alert['severity']}] {alert['reason']}", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "", 9)
            pdf.multi_cell(0, 5, txt=f"Time: {alert['timestamp']}\nProcess: {alert['process'].get('name', 'Unknown')} (PID: {alert['process'].get('pid', 'N/A')})\nPath: {alert['process'].get('exe', 'N/A')}\n")
            pdf.ln(2)
            
        pdf.output(report_path)
        return report_path
