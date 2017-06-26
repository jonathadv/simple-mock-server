#!/usr/bin/env python
import BaseHTTPServer
import json
import time


def load_configuration_file():
    file_name = 'simple_mock_server_conf.json'
    configuration = {}
    with open(file_name) as conf_file:
        json_config = json.loads(conf_file.read())
        configuration['hostname'] = json_config.get('hostname')
        configuration['port'] = json_config.get('port')

    return configuration

class SimpleHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        print 'Context: %s' % self.path
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write('')

    def do_POST(self):
        print 'Context: %s' % self.path
        self.send_response(200)


if __name__ == '__main__':
    config = load_configuration_file()
    hostname = config.get('hostname')
    port = config.get('port')

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((hostname, config.get('port')), SimpleHandler)

    print time.asctime(), "Server Starts - %s:%s" % (hostname, port)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print time.asctime(), 'Server Stops - %s:%s' % (hostname, port)
