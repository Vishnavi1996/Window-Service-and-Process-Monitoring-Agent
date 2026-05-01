from flask import Flask, render_template, jsonify
import threading
import logging

# Silence Flask logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class WebDashboard:
    def __init__(self, agent):
        self.agent = agent
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/api/alerts')
        def get_alerts():
            return jsonify(self.agent.logger.get_alerts())

        @self.app.route('/api/processes')
        def get_processes():
            return jsonify(self.agent.last_processes)

    def run(self, port=5000):
        # Run in a separate thread to not block the agent
        thread = threading.Thread(target=lambda: self.app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False), daemon=True)
        thread.start()
        print(f"[*] Web Dashboard active at http://localhost:{port}")
