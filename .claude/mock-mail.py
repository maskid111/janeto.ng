# Local mock of send-mail.php, for testing the front-end only (PHP isn't installed on this machine).
# name=fail -> 500 JSON, name=nophp -> raw PHP source as text (like a host without PHP), anything else -> {"ok": true}
import functools
import http.server
import json
import os
import re
import sys

ROOT = sys.argv[1]
FIELD = re.compile(r'name="([^"]+)"\r\n\r\n(.*?)\r\n--', re.S)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if not self.path.startswith('/send-mail.php'):
            self.send_error(404)
            return
        raw = self.rfile.read(int(self.headers.get('Content-Length', 0))).decode('utf8', 'replace')
        data = dict(FIELD.findall(raw))
        print('POST', data, flush=True)
        name = data.get('name', '')
        if name == 'nophp':
            body, ctype, code = b'<?php // source served as text', 'text/plain', 200
        elif name == 'fail':
            body, ctype, code = json.dumps({'ok': False, 'error': 'x'}).encode(), 'application/json', 500
        else:
            body, ctype, code = json.dumps({'ok': True}).encode(), 'application/json', 200
        self.send_response(code)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


http.server.ThreadingHTTPServer(('localhost', int(os.environ.get('PORT', 8124))), functools.partial(Handler, directory=ROOT)).serve_forever()
