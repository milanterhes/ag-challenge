from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class HookHandler(BaseHTTPRequestHandler):
    def challengeResponse(self, challenge):
        #response for slack
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        print(challenge)
        self.wfile.write(challenge)

    def verify_lead(self, msg):
        text = msg["event"]["text"]
        if "to" in text or "from" in text or "email" in text:
            print(json.loads(text))

    def do_POST(self):
        request_length = int(self.headers.get('Content-Length'))
        raw_req = self.rfile.read(request_length).decode('utf-8')
        message = json.loads(raw_req)
        
        #self.challengeResponse(bytes(request_json['challenge'], 'utf-8'))
        self.send_response(200)
        self.end_headers()
        #print('received event: ', request_json["event"]["text"], request_json["event_time"])
        
        if message["event"]["channel"] == "CDQPMC7PY":
            self.verify_lead(message)




def run(server_class=HTTPServer, handler_class=HookHandler):
    server_adress = ('', 80)
    httpd = server_class(server_adress, handler_class)
    print("launching server...")
    httpd.serve_forever()

run()

