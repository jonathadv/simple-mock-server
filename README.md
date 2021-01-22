[![license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/jonathadv/simple-mock-server)
[![python versions](https://img.shields.io/badge/python-2.6,%202.7-blue.svg)](https://github.com/jonathadv/simple-mock-server)
[![Build Status](https://api.travis-ci.org/jonathadv/simple-mock-server.svg?branch=master)](https://travis-ci.org/jonathadv/simple-mock-server)

# Simple Mock Server
Simple server to mock HTTP response.

This project aims to be a simple HTTP server easy and fast to setup, which you can run anywhere with Python 2 installed, and with all the useful resources in a mock server.

No `pip install`, no dependencies! Just run it as regular Python 2 script.

### Features
* Support methods GET, POST, PUT and DELETE.
* Any HTTP response code including the ability to HTTP redirect.
* Custom response body with any HTML/JSON/whatever-type you can put as string.
* Allow to load file from filesystem and send it as response.
* Custom header.
* CORS by adding the header `Access-Control-Allow-Origin`.
* Allow to set a delay to a specific call response (useful for timeout testing).

### Usage

This is a regular Python 2 script made to be run from the shell.

Basic usage is `./server.py`. The script will load the default configuration file called `config.json` from the same directory.

When starting, the script looks for *host* and *port* configuration following the below priority list:
1. Looks for `host` and `port` keys in the configuration file.
1. Looks for `HOST` and `PORT` environment variables.
1. Uses the fallback configuration `host = 0.0.0.0` and `port = 8000`.

To use a different configuration file, run the script with `-f` / `--file` option.

To see the help, run `./server.py -h` or `./server.py --help`.

```bash
usage: server.py [-h] [-f file]

optional arguments:
  -h, --help            show this help message and exit
  -f file, --file file  Use custom JSON configuration file.

ENVIRONMENT VARIABLES
        HOST
          Sets the host interface the server will use. It's overwritten by the configuration file.
          To use it, remove the key `host` from the configuration file.
        PORT
          Sets the port the server will listen on. It's overwritten by the configuration file.
          To use it, remove the key `port` from the configuration file.
```


#### Loading host and port from config.json
```bash
# Just run it
./server.py

Thu May 24 21:16:20 2018 Server Starts - 0.0.0.0:8000
127.0.0.1 - - [24/May/2018 21:16:31] "GET /status HTTP/1.1" 200 -
127.0.0.1 - - [24/May/2018 21:16:31] "POST /add HTTP/1.1" 200 -
127.0.0.1 - - [24/May/2018 21:16:31] "PUT /update HTTP/1.1" 200 -
127.0.0.1 - - [24/May/2018 21:16:31] "DELETE /remove HTTP/1.1" 200 -
127.0.0.1 - - [24/May/2018 21:16:31] "GET /redirect HTTP/1.1" 200 -

```

#### Loading host and port from environment
```bash
# Set the variables HOST and PORT
HOST=127.0.0.1 PORT=8000 ./server.py

Thu May 24 21:16:20 2018 Server Starts - 127.0.0.1:8080
127.0.0.1 - - [24/May/2018 21:16:31] "GET /status HTTP/1.1" 200 -
127.0.0.1 - - [24/May/2018 21:16:31] "POST /add HTTP/1.1" 200 -
127.0.0.1 - - [24/May/2018 21:16:31] "PUT /update HTTP/1.1" 200 -
127.0.0.1 - - [24/May/2018 21:16:31] "DELETE /remove HTTP/1.1" 200 -
127.0.0.1 - - [24/May/2018 21:16:31] "GET /redirect HTTP/1.1" 200 -

```

#### Loading custom configuration file
```bash
./server.py -f /some/path/custom.json
Loading "custom.json"...
Thu May 24 21:16:20 2018 Server Starts - 0.0.0.0:8000
127.0.0.1 - - [24/May/2018 21:16:31] "GET /status HTTP/1.1" 200 -
127.0.0.1 - - [24/May/2018 21:16:31] "POST /add HTTP/1.1" 200 -
127.0.0.1 - - [24/May/2018 21:16:31] "PUT /update HTTP/1.1" 200 -
127.0.0.1 - - [24/May/2018 21:16:31] "DELETE /remove HTTP/1.1" 200 -
127.0.0.1 - - [24/May/2018 21:16:31] "GET /redirect HTTP/1.1" 200 -


```


### Test the server's default  setup

You can test the server's default setup by running the file `./test/test.sh` right after clonig the project:
```bash
./test.sh
Reading configuration file 'config.json'...
Testing calls against http://127.0.0.1:8000...

[HTTP Methods]
{ "type":"GET", "status": "OK" }
{ "type":"POST", "status": "Created!" }
{ "type":"PUT", "status": "updated!" }
{ "type":"DELETE", "status": "Removed!" }

[Redirect]
HTTP/1.0 302 Found
Server: BaseHTTP/0.3 Python/2.7.6
Date: Mon, 10 Jul 2017 21:41:30 GMT
Content-Type: application/json
location: https://github.com/jonathadv/simple-mock-server
Content-length: 19
Proxy-Connection: keep-alive
Connection: keep-alive

[Attachment]
HTTP/1.0 200 OK
Server: BaseHTTP/0.3 Python/2.7.6
Date: Mon, 10 Jul 2017 21:41:30 GMT
Content-Disposition: attachment; filename="LICENSE.txt"
Content-length: 1070
Proxy-Connection: keep-alive
Connection: keep-alive

[Delayed call]
{ "type":"GET", "delay": 5 }
real    0m5.024s
user    0m0.005s
sys     0m0.004s

```
### Writing a mock

The file `config.json` contains all mocks information and may contain `host` and `port` settings as well.
To create a new mock, change `config.json` following the examples.

```
{
    "method":"GET",                                              <-- HTTP method you want to use
    "path":"/",                                                  <-- Path you want to mock
    "responseCode":200,                                          <-- HTTP code you want to return
    "body":"<html><head></head><title>Hello</h1></body></html>", <-- Content to be sent in the response body
    "delay": 5                                                   <-- The time in seconds this call will wait before returning (optional)
    "headers":[                                                  <-- The list of headers (can be an empty array)
        {
            "Content-Type":"text/html; charset=UTF-8"
        }
    ]
}
```
### Loading files from filesystem
To load files from filesystem, fill the `body` property with the notation ` @file://` followed by the file path. Like: `body: "@file:///home/user/my_pic.png"`.
You can manipulate the browser behavior when downloading the file by using the headers like `"Content-Type":"image/png"` and `"Content-Disposition": "attachment; filename=\"my_pic.png\""` and so on.

**Example #1**
Downloading a regular file (Browser may decide to display it).
```
{
    "method":"GET",
    "path":"/my_pic.png",
    "responseCode":200,
    "body":"@file:///home/user/my_pic.png",
    "headers":[
        {
            "Content-Type": "image/png"
        }
    ]
}
```

**Example #2**
Downloading the file as attachment.
```
{
    "method":"GET",
    "path":"/attachment",
    "responseCode":200,
    "body":"@file:///home/user/my_pic.png",
    "headers":[
        {
            "Content-Disposition": "attachment; filename=\"my_pic.png\""
        }
    ]
}
```


### Configuration file sample
```json
{

    "hostname":"0.0.0.0",
    "port":8000,
    "responses":[
        {
            "method":"GET",
            "path":"/",
            "responseCode":200,
            "body":"<html><head></head><title>Simple Mock Server test</title><body><h1>GET! It works!</h1></body></html>",
            "headers":[
                {
                    "Content-Type":"text/html; charset=UTF-8"
                }
            ]
        },
        {
            "method":"GET",
            "path":"/cors-test",
            "body":"{ \"type\":\"GET\", \"status\": \"OK\", \"message\": \"CORS worked!\" }",
            "responseCode":200,
            "headers":[
                {
                   "Access-Control-Allow-Origin":"*"
                },
                {
                    "Content-Type":"text/html; charset=UTF-8"
                }
            ]
        },

        {
            "method":"GET",
            "path":"/status",
            "responseCode":200,
            "body":"{ \"type\":\"GET\", \"status\": \"OK\" }",
            "headers":[
                {
                    "Content-Type":"application/json"
                }
            ]
        },
        {
            "method":"GET",
            "path":"/redirect",
            "responseCode":302,
            "body":"{\"type\":\"redirect\"}",
            "headers":[
                {
                    "Content-Type":"application/json"
                },
                {
                    "location":"https://github.com/jonathadv/simple-mock-server"
                }
            ]
        },
        {
            "method":"GET",
            "path":"/attachment",
            "responseCode":200,
            "body":"@file://./LICENSE.txt",
            "headers":[
                {
                    "Content-Disposition": "attachment; filename=\"LICENSE.txt\""
                }
            ]
        },
        {
            "method":"POST",
            "path":"/add",
            "responseCode":201,
            "body":"{ \"type\":\"POST\", \"status\": \"Created!\" }",
            "headers":[
                {
                    "Content-Type":"application/json"
                }
            ]
        },
        {
            "method":"PUT",
            "path":"/update",
            "responseCode":200,
            "body":"{ \"type\":\"PUT\", \"status\": \"updated!\" }",
            "headers":[
                {
                    "Content-Type":"application/json"
                }
            ]
        },
        {
            "method":"DELETE",
            "path":"/remove",
            "responseCode":200,
            "body":"{ \"type\":\"DELETE\", \"status\": \"Removed!\" }",
            "headers":[
                {
                    "Content-Type":"application/json"
                }
            ]
        }
    ]

}

```
