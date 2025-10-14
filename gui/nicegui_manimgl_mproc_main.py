# top of your scene file
from manimlib import *
import threading, json
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from queue import Queue, Empty


import subprocess, sys, pathlib
subprocess.Popen([sys.executable, str(pathlib.Path(__file__).with_name('ui_app.py'))])


CMD_Q = Queue()

class CmdHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/cmd':
            self.send_response(404); self.end_headers(); return
        ln = int(self.headers.get('Content-Length','0'))
        data = self.rfile.read(ln)
        try:
            msg = json.loads(data.decode('utf-8'))
            CMD_Q.put(msg)
            self.send_response(204); self.end_headers()
        except Exception as e:
            self.send_response(400); self.end_headers()
            self.wfile.write(str(e).encode())

    def log_message(self, *args):  # silence server logs
        pass

def start_cmd_server(port=5050):
    srv = ThreadingHTTPServer(('127.0.0.1', port), CmdHandler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv

class Demo(Scene):
    def construct(self):
        start_cmd_server(5050)           # start local API
        self.m = Circle(); self.add(self.m)

        while True:
            try:
                msg = CMD_Q.get_nowait()
            except Empty:
                self.wait(0.05); continue

            c = msg.get('cmd'); kw = msg.get('kwargs', {})
            if c == 'add_square':
                self.add(Square())
            elif c == 'rotate':
                self.play(Rotate(self.m, kw.get('angle', PI/6)))
            elif c == 'fade_in':
                self.play(FadeIn(self.m))
            elif c == 'quit':
                break
            self.wait(0.05)
