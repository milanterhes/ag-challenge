from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3

class HookHandler(BaseHTTPRequestHandler):
    def challengeResponse(self, challenge):
        #response for slack
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        print(challenge)
        self.wfile.write(challenge)

    def handle_event(self, msg):
        if msg["event"]["channel"] == "CDQPMC7PY":

            text = msg["event"]["text"] #message sent by the user
            date = {"date": msg["event_time"]}
            text.update(date)

            if "to" in text or "from" in text or "email" in text:
                print(text)

                #save 
                conn = sqlite3.connect('example.db')
                c = conn.cursor()
                c.execute("""CREATE TABLE if not exists flights(
                                start TEXT,
                                destination TEXT NOT NULL,
                                email TEXT NOT NULL,
                                date integer NOT NULL
                                );""")
                new_record = (text["from"], text["to"], text["email"], text["date"])
                c.execute("INSERT INTO flights VALUES(?,?,?,?);",new_record)
                conn.commit()
                c.close()

    def do_POST(self):
        #get the body of the request
        request_length = int(self.headers.get('Content-Length'))
        raw_req = self.rfile.read(request_length).decode('utf-8')
        message = json.loads(raw_req)
        
        #this had to be ran only once for slack to authenticate
        #self.challengeResponse(bytes(request_json['challenge'], 'utf-8'))

        #200 response needed for slack otherwise it sends the event multiple times
        self.send_response(200)
        self.end_headers()

        self.handle_event(message)

def run(server_class=HTTPServer, handler_class=HookHandler):
    server_adress = ('', 8080)
    httpd = server_class(server_adress, handler_class)
    print("launching server...")
    httpd.serve_forever()

run()
