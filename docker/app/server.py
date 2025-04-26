from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading


vehicles_data = {}
lock = threading.Lock()

class OpenTTDHandler(BaseHTTPRequestHandler):

    # Expose POST to receive data
    def do_POST(self):
        if self.path == "/api/openttd/metrics":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                print("RECEIVED "+str(post_data))
                data = json.loads(post_data)
                vehicle_name = data.get("vehicle_name", None)
                if vehicle_name is not None:
                    with lock:
                        vehicles_data[vehicle_name] = data
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'OK')
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Missing vehicle_name')
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid JSON')

    # Expose prometheus compatible Endpoint
    def do_GET(self):
        if self.path == "/metrics":
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain; version=0.0.4')
            self.end_headers()

            metrics = []
            with lock:
                for vehicle_name, entry in vehicles_data.items():
                    # Una metrica per ogni veicolo, solo l'ultima ricevuta
                    metric = (
                        f'openttd_vehicle_value{{'
                        f'company_id="{entry.get("company_id", "unknown")}",'
                        f'vehicle_name="{vehicle_name}",'
                        f'vehicle_type="{entry.get("vehicle_type", "unknown")}"'
                        f'}} {entry.get("profit_this_year", 0)}'
                    )
                    metrics.append(metric)

            response = "\n".join(metrics)
            self.wfile.write(response.encode())

def run():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, OpenTTDHandler)
    print('Server running on http://localhost:8080...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
