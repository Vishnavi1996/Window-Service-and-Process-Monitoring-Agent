from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from datetime import datetime
import time

class CLIDashboard:
    def __init__(self, agent):
        self.console = Console()
        self.agent = agent

    def generate_layout(self):
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        layout["body"].split_row(
            Layout(name="processes"),
            Layout(name="alerts")
        )
        return layout

    def get_process_table(self):
        table = Table(title="Top Processes", box=None)
        table.add_column("PID", style="cyan")
        table.add_column("Name", style="magenta")
        table.add_column("CPU %", justify="right")
        table.add_column("Memory %", justify="right")
        
        # Limit to top 15 processes for UI
        for p in self.agent.last_processes[:15]:
            table.add_row(
                str(p.get('pid', '')),
                p.get('name', ''),
                "0.0", # Placeholder
                "0.0"  # Placeholder
            )
        return table

    def get_alert_panel(self):
        alerts = self.agent.logger.get_alerts()[-10:] # Last 10 alerts
        alert_text = ""
        for alert in reversed(alerts):
            color = "white"
            if alert['severity'] == "CRITICAL": color = "red"
            elif alert['severity'] == "HIGH": color = "orange1"
            elif alert['severity'] == "MEDIUM": color = "yellow"
            
            alert_text += f"[{color}][{alert['severity']}] {alert['reason']}[/{color}]\n"
            
        return Panel(alert_text, title="Recent Alerts", border_style="red")

    def run(self):
        layout = self.generate_layout()
        layout["header"].update(Panel(f"Windows Security Agent - {datetime.now().strftime('%H:%M:%S')}", style="bold blue"))
        layout["footer"].update(Panel("Press Ctrl+C to exit | Monitoring in progress...", style="dim"))
        
        with Live(layout, refresh_per_second=1, screen=True):
            while True:
                layout["header"].update(Panel(f"Windows Security Agent - {datetime.now().strftime('%H:%M:%S')}", style="bold blue"))
                layout["processes"].update(Panel(self.get_process_table(), title="Process List"))
                layout["alerts"].update(self.get_alert_panel())
                time.sleep(2)
