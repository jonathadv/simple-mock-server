#!/usr/bin/env python
import BaseHTTPServer
import json
import time
import httplib

class Configuration():
    def __init__(self, hostname, port, responses):
        self.hostname = hostname
        self.port = port
        self.get_response_map = self.build_response_map([r for r in responses if r.get('method') == 'GET'])
        self.post_response_map = self.build_response_map([r for r in responses if r.get('method') == 'POST'])
        self.put_response_map = self.build_response_map([r for r in responses if r.get('method') == 'PUT'])
        self.delete_response_map = self.build_response_map([r for r in responses if r.get('method') == 'DELETE'])

    @staticmethod
    def build_response_map(responses):
        response_map = {}
        for response in responses:
            response_map[response.get('path')] = MokedResponse(
                response.get('method'), response.get('path'),
                response.get('responseCode'), response.get('headers'),
                response.get('body'))

        return response_map

class MokedResponse():
    def __init__(self, method='GET', path='/', responseCode=200,
                 headers=None, body=None):

        self.method = method
        self.path = path
        self.responseCode = responseCode
        self.headers = headers
        self.body = body

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'method = [%s], path = [%s], responseCode = [%s], ' \
               'headers = [%s], body = [%s]' % \
               (self.method, self.path, self.responseCode, self.headers, self.body)

def SimpleHandlerFactory(configuration):
    class SimpleHandler(BaseHTTPServer.BaseHTTPRequestHandler):
        response_map = {
            "GET": configuration.get_response_map.get,
            "POST": configuration.post_response_map.get,
            "PUT": configuration.put_response_map.get,
            "DELETE": configuration.delete_response_map.get
        }

        def do_HEAD(self):
            self.send_response(httplib.OK)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        def do_GET(self):
            response = self.retrive_response(self.path, 'GET')
            self.send(self.path, response)

        def do_POST(self):
            response = self.retrive_response(self.path, 'POST')
            self.send(self.path, response)

        def do_DELETE(self):
            response = self.retrive_response(self.path, 'DELETE')
            self.send(self.path, response)

        def do_PUT(self):
            response = self.retrive_response(self.path, 'PUT')
            self.send(self.path, response)

        def send(self, path, response):
            self.send_response(response.responseCode)

            for header in response.headers:
                self.send_header(header.keys()[0], header.values()[0])

            self.end_headers()
            self.wfile.write(response.body)


        def retrive_response(self, path, method):
            try:
                response = self.response_map.get(method)(path)

                if response is None:
                    body = "{ \"message\": \"path '%s' not found\" }" % path
                    headers = [{"Content-Type": "Application/JSON"}]
                    response = MokedResponse(method, path, 404, headers, body)

            except Exception as err:
                body = "{ \"message\": \"Some error happened while getting path '%s'\", \"cause\": \"%s\" }" % (path, str(err))
                headers = [{"Content-Type": "Application/JSON"}]
                response = MokedResponse(method, path, 500, headers, body)

            return response


    return SimpleHandler

def load_configuration_file():
    file_name = 'simple_mock_server_conf.json'
    with open(file_name) as conf_file:
        json_config = json.loads(conf_file.read())
        configuration = Configuration(json_config.get('hostname'), json_config.get('port'),
                                      json_config.get('responses'))


    return configuration

if __name__ == '__main__':
    config = load_configuration_file()

    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((config.hostname, config.port), SimpleHandlerFactory(config))

    print time.asctime(), "Server Starts - %s:%s" % (config.hostname, config.port)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print time.asctime(), 'Server Stops - %s:%s' % (config.hostname, config.port)
