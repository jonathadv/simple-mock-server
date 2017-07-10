#!/usr/bin/env bash

config_file=simple_mock_server_conf.json

if [[ ! -f "${config_file}" ]]; then
    echo "file ''${config_file}' not found. Nothing to do. Exiting."
    exit 1
fi

echo "Reading configuration file '${config_file}'..."

host=$(egrep '"hostname"' ${config_file} | cut -d ':' -f 2 | sed 's/[",]//g')
port=$(egrep '"port":[0-9]+' ${config_file} | cut -d ':' -f 2 | sed 's/[^0-9]//g' | sed 's/[^0-9]//g')

if [[ -z  "${host}" || -z "${port}" ]]; then
    echo "Unable to get host or port from file '${config_file}''. Nothing to do. Exiting."
    exit 1
fi

echo "Testing calls against http://${host}:${port}..."
echo

echo '[HTTP Methods]'
curl -X GET http://${host}:${port}/status; echo
curl -X POST http://${host}:${port}/add; echo
curl -X PUT http://${host}:${port}/update; echo
curl -X DELETE http://${host}:${port}/remove; echo

echo
echo '[Redirect]'
curl -I -X GET http://${host}:${port}/redirect; 

echo '[Attachment]'
curl -I -X GET http://${host}:${port}/attachment;

echo '[Delayed call]'
time curl -X GET http://${host}:${port}/delay; echo