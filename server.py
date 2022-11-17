from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import warnings
import pdf_tables_parse
import shutil
import os


warnings.simplefilter("ignore")

hostName = "127.0.0.1"
serverPort = 8001
pdf = pdf_tables_parse

class App(BaseHTTPRequestHandler):
    def do_POST(self):
        os.mkdir('./pdf_tables_parse/in/')
        content_len = int(self.headers.get('Content-Length'))
        post_body = self.rfile.read(content_len)
        with open('./pdf_tables_parse/in/temp.pdf', 'wb') as out:
            out.write(post_body)

        type = str(self.headers.get('Type'))
        print(type)
        try:
            data = pdf.start('./pdf_tables_parse/in/temp.pdf', type)
        except Exception as e:
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({"error": e}), "utf-8"))
            return 0

        self.send_response(200)
        self.send_header("Content-type", "text/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(data), "utf-8"))
        shutil.rmtree('./pdf_tables_parse/in/')



if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), App)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
