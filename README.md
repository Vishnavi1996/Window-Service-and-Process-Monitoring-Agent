# 🛡️ Windows Service & Process Monitoring Agent

A comprehensive, modular Blue Team security tool designed to monitor Windows processes and services in real-time. It detects suspicious behavior, persistence mechanisms, and potential malware activity using a rule-based detection engine.

## 🚀 Features

### 🔍 Monitoring & Detection
- **Process Monitoring**: Real-time tracking of PID, PPID, executable paths, and user context.
- **Parent-Child Analysis**: Detects suspicious chains (e.g., `winword.exe` → `powershell.exe`).
- **Name Mimicking**: Identifies processes mimicking system files (e.g., `svch0st.exe` vs `svchost.exe`).
- **Risk Directory Detection**: Flags processes running from `Temp`, `Downloads`, and `AppData`.
- **Service Auditing**: Monitors Windows services for unusual binary paths and suspicious names.

### 🖥️ Multiple Interfaces
- **Command Line (CLI)**: A beautiful, live-updating terminal dashboard.
- **Desktop (GUI)**: A Windows-native dashboard for easy management and report generation.
- **Web Dashboard**: A modern, responsive web interface for remote or local monitoring.

### 📊 Reporting & Logging
- **Structured Logging**: All events are stored in `logs/alerts.json` and `logs/agent.log`.
- **Automated Reports**: Generate comprehensive PDF and Text summaries of detected threats.

---

## 🛠️ Architecture

The system is built with a modular Python architecture:

- `core/detection_engine.py`: The "brain" containing security rules and risk logic.
- `core/process_monitor.py`: Handles `psutil` based process enumeration.
- `core/service_audit.py`: Audits Windows services for anomalies.
- `ui/`: Contains the logic for CLI (Rich), GUI (Tkinter), and Web (Flask) interfaces.
- `main.py`: The central orchestrator.

---

## 📥 Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "window Service and Process Monitoring Agent"
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 📖 Usage

Run the agent using `main.py` with the `--mode` flag:

### 1. Command Line Mode
```bash
python main.py --mode cli
```

### 2. Desktop GUI Mode
```bash
python main.py --mode gui
```

### 3. Web Dashboard Mode
```bash
python main.py --mode web
```
*Once started, visit `http://localhost:5000` in your browser.*

### 4. Run All (Web + GUI)
```bash
python main.py --mode all
```

---

## 🛡️ Detection Rules

The agent currently implements the following security checks:
| Severity | Rule Name | Description |
| :--- | :--- | :--- |
| **CRITICAL** | Blacklist Detection | Known malicious process names. |
| **HIGH** | Suspicious Chain | Legitimate apps spawning shells or scripts. |
| **HIGH** | Name Mimicking | Levenshtein-based similarity to core system files. |
| **MEDIUM** | Risk Directory | Execution from user-writable/temporary folders. |
| **LOW** | Unknown Location | Execution from non-standard program directories. |

---

## 📝 Disclaimer
This tool is intended for educational and security research purposes. While it can detect many common threats, it is not a replacement for a full-scale EDR/AV solution.

## 📄 License
MIT License
