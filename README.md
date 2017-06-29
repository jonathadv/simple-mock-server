# simple-mock-server
Simple server to mock HTTP response

The idea is to have the simplest HTTP server with the simplest configuration, which can run anywhere with Python2 installed, and with all the useful resources in a mock server.

No `pip install`, no high-version-specific dependencies! Just run it as regular Python 2 script

### Features
* Support to methods GET, POST, PUT and DELETE.
* Support to any HTML/JSON/String-whatever you can put as string (maybe some string encoding issue can come up).
* Support to any HTTP response code including the ability to HTTP redirect.

### Requirements
* Python 2.7 (tested in Python 2.7.9)

### Usage
```bash
# Run as a regular python script
   ./simple-mock-server.py
```
### Before running it
Open the configuration file `simple_mock_server_conf.json` and fill it with your mock data following the examples.


---
### Configuration file sample
```
{

    "hostname":"127.0.0.1",
    "port":8080,
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
            "path":"/status",
            "responseCode":200,
            "body":"{ \"type\":\"GET\", \"status\": \"OK\" }",
            "headers":[
                {
                    "Content-Type":"Application/JSON"
                }
            ]
        },
        {
            "method":"GET",
            "path":"/redirect",
            "responseCode":302,
            "body":null,
            "headers":[
                {
                    "location":"https://github.com/jonathadv/simple-mock-server"
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
                    "Content-Type":"Application/JSON"
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
                    "Content-Type":"Application/JSON"
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
                    "Content-Type":"Application/JSON"
                }
            ]
        }
    ]

}

```
---
### TODO List
* Support to path variable like `/some/{variable}/path`
* Code documentation
* Test encoding support
* Add support to reply with binary content