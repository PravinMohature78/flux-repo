import os, subprocess
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
class Handler(BaseHTTPRequestHandler):
    def handle_git(self):
        path = urlsplit(self.path)
        env = os.environ.copy()
        env.update(GIT_PROJECT_ROOT='/repos', GIT_HTTP_EXPORT_ALL='1', PATH_INFO=path.path,
                   QUERY_STRING=path.query, REQUEST_METHOD=self.command,
                   CONTENT_TYPE=self.headers.get('Content-Type',''),
                   CONTENT_LENGTH=self.headers.get('Content-Length','0'),
                   REMOTE_ADDR=self.client_address[0])
        if self.headers.get('Git-Protocol'): env['HTTP_GIT_PROTOCOL']=self.headers['Git-Protocol']
        body=self.rfile.read(int(env['CONTENT_LENGTH']))
        p=subprocess.run(['git','http-backend'],input=body,stdout=subprocess.PIPE,env=env)
        head, _, payload=p.stdout.partition(b'\r\n\r\n')
        if not _: self.send_error(502); return
        headers=[]; status=200
        for line in head.decode().split('\r\n'):
            key,value=line.split(':',1)
            if key.lower()=='status': status=int(value.strip().split()[0])
            else: headers.append((key,value.strip()))
        self.send_response(status)
        for key,value in headers: self.send_header(key,value)
        self.end_headers(); self.wfile.write(payload)
    do_GET=handle_git
    do_POST=handle_git
ThreadingHTTPServer(('0.0.0.0',8000),Handler).serve_forever()
