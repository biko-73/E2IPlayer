# -*- coding: utf-8 -*-


from urllib.request import Request, urlopen, build_opener, install_opener
import sys
import time
import traceback
import socketserver
from http.server import SimpleHTTPRequestHandler

import signal
import os


def signal_handler(sig, frame):
    os.kill(os.getpid(), signal.SIGTERM)


signal.signal(signal.SIGINT, signal_handler)


def printExc(msg=''):
    msg = 'EXCEPTION: \n%s' % traceback.format_exc()
    print(msg)


def getPage(url, params={}, post_data=None):
    sts = False
    data = None
    return_data = params.get('return_data', True)
    try:
        req = Request(url, post_data, params)
        if 'Referer' in params:
            req.add_header('Referer', params['Referer'])
        if 'User-Agent' in params:
            req.add_header('User-Agent', params['User-Agent'])
        if 'Connection' in params:
            req.add_header('Connection', params['Connection'])
        resp = urlopen(req)
        if return_data:
            data = resp.read()
            resp.close()
        else:
            data = resp
        sts = True
    except Exception:
        printExc()
    return sts, data


HTTP_HEADER = {'Connection': 'keep-alive', 'return_data': False}


class Proxy(SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            url = self.path

            if url.startswith('/https/'):
                url = 'https://' + url[7:]
            elif url.startswith('/http/'):
                url = 'http://' + url[6:]

            sts, resp = getPage(url, HTTP_HEADER)
            if sts:
                self.send_response(200)
                self.end_headers()
                self.copyfile(resp, self.wfile)
            else:
                self.send_response(403)
                self.end_headers()
        except KeyboardInterrupt:
            self.server._BaseServer__shutdown_request = True

    def log_request(self, code='-', size='-'):
        pass

    def log_error(self, format, *args):
        pass


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print('libsPath, userAgent, refererUrl and m3u8Url are needed', file=sys.stderr)
        sys.exit(1)

    try:
        port = int(sys.argv[1])
        libsPath = sys.argv[2]
        userAgent = sys.argv[3]
        refererUrl = sys.argv[4]
        m3u8Url = sys.argv[5]

        sys.path.insert(1, libsPath)
        from keepalive import HTTPHandler
        keepalive_handler = HTTPHandler()
        opener = build_opener(keepalive_handler)
        install_opener(opener)

        HTTP_HEADER.update({'User-Agent': userAgent, 'Referer': refererUrl})
        socketserver.TCPServer.allow_reuse_address = True
        httpd = socketserver.TCPServer(('127.0.0.1', port), Proxy)
        port = httpd.server_address[1]
        print('\nhttp://127.0.0.1:%s/%s\n' % (port, m3u8Url.replace('://', '/', 1)), file=sys.stderr)
        httpd.serve_forever()
    except KeyboardInterrupt:
        printExc()
        httpd.shutdown()
        httpd.socket.close()
        httpd.server_close()
    sys.exit(0)
