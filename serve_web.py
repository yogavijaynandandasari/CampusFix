"""
serve_web.py - Lightweight Web Server and REST API Bridge for CampusFix
Serves the modern redesigned single-page application and syncs live with SQLite & Pandas.
Zero external dependencies required (uses standard library http.server).
Automatically opens the user's default web browser on launch.
"""

import http.server
import json
import os
import socketserver
import sys
import threading
import urllib.parse
import webbrowser

# Ensure local project path is accessible
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

import database as db
import analysis

PORT = 8000
INDEX_HTML_PATH = os.path.join(BASE_DIR, "index.html")


class CampusFixHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        # Route: Main Application Page
        if path in ["/", "/index.html"]:
            self.serve_index()
            return

        # API Route: Get All Complaints
        elif path == "/api/complaints":
            self.send_json_response(db.get_all_complaints())
            return

        # API Route: Get All Maintenance Records
        elif path == "/api/maintenance":
            self.send_json_response(db.get_all_maintenance_records())
            return

        # API Route: Get Analytical Metrics (Pandas-powered)
        elif path == "/api/metrics":
            metrics = analysis.calculate_metrics()
            self.send_json_response(metrics)
            return

        # API Route: Trigger Pandas CSV Export
        elif path == "/api/export-csv":
            success, filepath = analysis.export_to_csv()
            self.send_json_response({"success": success, "filepath": filepath})
            return

        # Route: Download Complaints Report CSV
        elif path in ["/reports/complaints_report.csv", "/api/download-csv"]:
            report_path = os.path.join(BASE_DIR, "reports", "complaints_report.csv")
            if not os.path.exists(report_path):
                analysis.export_to_csv()
            if os.path.exists(report_path):
                with open(report_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Disposition", 'attachment; filename="complaints_report.csv"')
                self.send_header("Content-Length", str(len(content)))
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(content)
                return

        # Default static file handler
        return super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        # Read JSON body
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        # API Route: Register Complaint
        if path == "/api/complaints":
            student_name = data.get("student_name", "")
            department = data.get("department", "")
            building = data.get("building", "")
            room_no = data.get("room_no", "")
            category = data.get("category", "")
            problem = data.get("problem", "")
            priority = data.get("priority", "Medium")

            new_id = db.add_complaint(
                student_name=student_name,
                department=department,
                building=building,
                room_no=room_no,
                category=category,
                problem=problem,
                priority=priority
            )
            self.send_json_response({"success": True, "complaint_id": new_id}, status=201)
            return

        # API Route: Add Maintenance Record
        elif path == "/api/maintenance":
            complaint_id = data.get("complaint_id", "")
            staff_name = data.get("staff_name", "")
            repair_date = data.get("repair_date", "")
            cost = float(data.get("cost", 0.0))
            remarks = data.get("remarks", "")

            db.add_maintenance_record(complaint_id, staff_name, repair_date, cost, remarks)
            self.send_json_response({"success": True, "message": "Maintenance logged"}, status=201)
            return

        self.send_error(404, "Endpoint not found")

    def do_PUT(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        # Read JSON body
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
        try:
            data = json.loads(body)
        except Exception:
            data = {}

        # API Route: Update Complaint Status (/api/complaints/<id>/status)
        if path.startswith("/api/complaints/") and path.endswith("/status"):
            parts = path.strip("/").split("/")
            complaint_id = parts[2]
            new_status = data.get("status", "Pending")
            db.update_complaint_status(complaint_id, new_status)
            self.send_json_response({"success": True, "complaint_id": complaint_id, "status": new_status})
            return

        self.send_error(404, "Endpoint not found")

    def serve_index(self):
        if not os.path.exists(INDEX_HTML_PATH):
            self.send_error(404, "index.html not found")
            return

        with open(INDEX_HTML_PATH, "rb") as f:
            content = f.read()

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_json_response(self, data, status=200):
        body = json.dumps(data, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)


def launch_browser(url):
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Note: Could not open browser automatically: {e}")


def run_server(port=PORT):
    # Initialize DB first
    db.init_db()

    # Enable socket reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), CampusFixHandler) as httpd:
        url = f"http://localhost:{port}"
        print("=" * 65)
        print("  CAMPUS MAINTENANCE COMPLAINT & TRACKING SYSTEM")
        print(f"  Browser Dashboard is live at: {url}")
        print("  Connected to SQLite DB: data/campus.db")
        print("  Automatically opening default web browser...")
        print("  Press Ctrl+C to stop the server.")
        print("=" * 65)

        # Trigger automatic browser opening in background after 0.5s
        timer = threading.Timer(0.5, launch_browser, args=[url])
        timer.daemon = True
        timer.start()

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer shutting down gracefully.")


if __name__ == "__main__":
    run_server()
