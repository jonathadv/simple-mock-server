# simple-mock-server
Simple server to mock HTTP response

The idea is to have the simplest HTTP server with the simplest configuration, which you can run anywhere with Python2 installed, and with all the useful resources in a mock server.

No `pip install`, no high-version-specific dependencies! Just run it as regular Python 2 script.

### Features
* Support to methods GET, POST, PUT and DELETE.
* Any HTTP response code including the ability to HTTP redirect.
* Custom response body with any HTML/JSON/whatever-type you can put as string (maybe some string encoding issue can come up).
* Allow to load file from filesystem and send it as response.
* Custom header.
* CORS by adding the header `Access-Control-Allow-Origin`.
* Allow to set a delay to a specific call response (useful for timeout testing).

### Requirements
* Python 2.7 (tested with Python 2.7.5)

### Usage
```bash
# Run as a regular python script
./simple-mock-server.py

Thu Jun 29 02:00:41 2017 Server Starts - 127.0.0.1:8080
127.0.0.1 - - [29/Jun/2017 02:00:44] "GET /status HTTP/1.1" 200 -
127.0.0.1 - - [29/Jun/2017 02:00:44] "POST /add HTTP/1.1" 201 -
127.0.0.1 - - [29/Jun/2017 02:00:44] "PUT /update HTTP/1.1" 200 -
127.0.0.1 - - [29/Jun/2017 02:00:44] "DELETE /remove HTTP/1.1" 200 -
127.0.0.1 - - [29/Jun/2017 02:00:44] "GET /redirect HTTP/1.1" 302 -

```
You can test the server as it is by running the file `test-simple-mock-server.sh` right before getting it:
```bash
./test-simple-mock-server.sh
Reading configuration file 'simple_mock_server_conf.json'...
Testing calls against http://127.0.0.1:8080...

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


### Before running it for your own needs...
Open the configuration file `simple_mock_server_conf.json` and fill it with your mock data following the examples.


### Configuration file sample
```json
{

    "hostname":"127.0.0.1",
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
