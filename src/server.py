#!/usr/bin/env python

# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
Simple Mock Server
-------------------

Run as a regular python script:
$ ./server.py
"""

import argparse
import json
import os
import sys
import time

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler


class Configuration:
    def __init__(self, hostname, port, responses):
        self.hostname = hostname
        self.port = port
        self.get_response_map = {}
        self.post_response_map = {}
        self.put_response_map = {}
        self.delete_response_map = {}
        self._build_response_map(responses)

    def _build_response_map(self, responses):
        response_map = {
            "GET": self.get_response_map,
            "POST": self.post_response_map,
            "PUT": self.put_response_map,
            "DELETE": self.delete_response_map,
        }

        for response in responses:
            mocked_resp = MokedResponse(
                response.get("method"),
                response.get("path"),
                response.get("responseCode"),
                response.get("headers"),
                response.get("body"),
                response.get("delay"),
            )

            method_map = response_map[response.get("method").upper()]
            method_map[response.get("path")] = mocked_resp


class MokedResponse:
    def __init__(
        self,
        method=None,
        path=None,
        response_code=None,
        headers=None,
        body=None,
        delay=None,
    ):
        self.method = method if method else "GET"
        self.path = path if path else "/"
        self.response_code = response_code if response_code else 200
        self.headers = headers if headers else []
        self.delay = delay if delay else 0
        self.body = self.MokedResponseBody(body)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (
            "method = [%s], path = [%s], response_code = [%s], "
            "headers = [%s], body = [%s], delay = [%s]"
            % (
                self.method,
                self.path,
                self.response_code,
                self.headers,
                self.body,
                self.delay,
            )
        )

    class MokedResponseBody:
        def __init__(self, content=None):
            self._file_definition = "@file://"
            self.content = content if content else ""
            self.is_file = self._file_definition in content

        def load(self):
            if self.is_file:
                filename = self.content.replace(self._file_definition, "")
                try:
                    with open(filename) as file:
                        return file.read()
                except:
                    print >> sys.stderr, (
                        "File '%s' not found in filesystem." % filename
                    )
                    return None
            else:
                return self.content

        def __len__(self):
            try:
                filename = self.content.replace(self._file_definition, "")
                length = os.stat(filename).st_size
            except:
                length = len("None")

            return length if self.is_file else len(self.content)

        def __str__(self):
            return "is_file = [%s], content = [%s]" % (
                self.is_file,
                self.content,
            )


def SimpleHandlerFactory(configuration):
    class SimpleHandler(BaseHTTPRequestHandler):
        response_map = {
            "GET": configuration.get_response_map.get,
            "POST": configuration.post_response_map.get,
            "PUT": configuration.put_response_map.get,
            "DELETE": configuration.delete_response_map.get,
        }

        def do_HEAD(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        def do_GET(self):
            response = self.retrive_response(self.path, "GET")
            self.send(self.path, response)

        def do_POST(self):
            response = self.retrive_response(self.path, "POST")
            self.send(self.path, response)

        def do_DELETE(self):
            response = self.retrive_response(self.path, "DELETE")
            self.send(self.path, response)

        def do_PUT(self):
            response = self.retrive_response(self.path, "PUT")
            self.send(self.path, response)

        def send(self, path, response):
            time.sleep(response.delay)

            self.send_response(response.response_code)

            for header in response.headers:
                self.send_header(header.keys()[0], header.values()[0])
            self.send_header("Content-length", str(len(response.body)))
            self.end_headers()
            self.wfile.write(response.body.load())

        def retrive_response(self, path, method):
            try:
                response = self.response_map.get(method)(path)

                if response is None:
                    body = '{ "message": "path \'%s\' not found" }' % path
                    headers = [{"Content-Type": "Application/JSON"}]
                    response = MokedResponse(method, path, 404, headers, body)

            except Exception as err:
                body = (
                    '{ "message": "Some error happened while getting path \'%s\', "cause": "%s" }'
                    % (path, str(err))
                )
                headers = [{"Content-Type": "Application/JSON"}]
                response = MokedResponse(method, path, 500, headers, body)

            return response

    return SimpleHandler


def load_configuration(config_file=None):
    default_host = os.environ.get("HOST", "0.0.0.0")
    default_port = int(os.environ.get("PORT", "8000"))
    default_responses = []
    if config_file:
        print ('Loading "%s"...' % config_file)
        file_name = config_file
    else:
        print ("Loading default config.json...")
        file_name = "config.json"

    with open(file_name) as conf_file:
        json_config = json.loads(conf_file.read())

    configuration = Configuration(
        json_config.get("hostname", default_host),
        json_config.get("port", default_port),
        json_config.get("responses", default_responses),
    )

    return configuration


def main(config):
    httpd = HTTPServer(
        (config.hostname, config.port), SimpleHandlerFactory(config)
    )

    print time.asctime(), "Server Starts - %s:%s" % (
        config.hostname,
        config.port,
    )

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (
        config.hostname,
        config.port,
    )


def get_opts():
    env_var_msg = """ENVIRONMENT VARIABLES
    \tHOST
    \t  Sets the host interface the server will use. It's overwritten by the configuration file.
    \t  To use it, remove the key `host` from the configuration file.
    \tPORT
    \t  Sets the port the server will listen on. It's overwritten by the configuration file.
    \t  To use it, remove the key `port` from the configuration file.

    """
    parser = argparse.ArgumentParser(
        epilog=env_var_msg,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-f",
        "--file",
        metavar="file",
        help="Use custom JSON configuration file.",
        required=False,
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_opts()
    config = load_configuration(args.file)
    main(config)
