#!/usr/bin/env python
import BaseHTTPServer
import json
import time
import httplib

class Configuration(object):
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

class SimpleHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(httplib.OK)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        print 'Context: %s' % self.path
        self.send_response(httplib.OK)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write('')

    def do_POST(self):
        print 'Context: %s' % self.path
        self.send_response(httplib.OK)

def load_configuration_file():
    file_name = 'simple_mock_server_conf.json'
    with open(file_name) as conf_file:
        json_config = json.loads(conf_file.read())
        configuration = Configuration(json_config.get('hostname'), json_config.get('port'))

    return configuration

if __name__ == '__main__':
    config = load_configuration_file()

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((config.hostname, config.port), SimpleHandler)

    print time.asctime(), "Server Starts - %s:%s" % (config.hostname, config.port)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print time.asctime(), 'Server Stops - %s:%s' % (config.hostname, config.port)
