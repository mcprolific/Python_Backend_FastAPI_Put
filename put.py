from http.server import BaseHTTPRequestHandler, HTTPServer
import json

data = [
    {
        "name": "Saka Idris", 
        "age": 25, 
        "track": "AI Developer"
    }
]

class BasicAPI(BaseHTTPRequestHandler):
    def send_data(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_PUT(self):
        try:
            index = int(self.path.strip("/"))
            if index < 0 or index >= len(data):
                self.send_data(404)
                self.wfile.write(json.dumps({"error": "Item not found"}).encode())
                return

            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            updated_info = json.loads(body.decode())

            data[index].update(updated_info)
            self.send_data(200)
            self.wfile.write(json.dumps({
                "message": "Item updated successfully",
                "updated_item": data[index]
            }).encode())
        except Exception as e:
            self.send_data(400)
            self.wfile.write(json.dumps({"error": str(e)}).encode())

def run():
    print("Application is running on http://localhost:5000")
    HTTPServer(('localhost', 5000), BasicAPI).serve_forever()

run()
