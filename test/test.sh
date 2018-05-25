#!/usr/bin/env bash

set -e

declare -r base_dir="$( cd "$(dirname "$0")/.." ; pwd -P )"
declare -r config_file="${base_dir}/src/config.json"

if [[ ! -f "${config_file}" ]]; then
    echo "file ''${config_file}' not found. Nothing to do. Exiting."
    exit 1
fi


function start_server() {
    echo "Starting server..."
    python ${base_dir}/src/server.py -f ${config_file} &
    sleep 2
}

function stop_server() {
    echo -n "Stopping server.."
    kill "$(pidof python)"
    echo "[OK]"
}


function test() {
    echo "Reading configuration file '${config_file}'..."

    host=$(egrep '"hostname"' ${config_file} | cut -d ':' -f 2 | sed 's/[",]//g')
    port=$(egrep '"port":[0-9]+' ${config_file} | cut -d ':' -f 2 | sed 's/[^0-9]//g' | sed 's/[^0-9]//g')

    if [[ -z  "${host}" || -z "${port}" ]]; then
        echo "Unable to get host or port from file '${config_file}''. Nothing to do. Exiting."
        exit 1
    fi

    if [[ "${host}" == '0.0.0.0' ]]; then
        echo 'Server is listening in all interfaces, setting host as 127.0.0.1'
        host='127.0.0.1'
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
}

if [[ "$1" == "--start-server" ]]; then
    start_server
    test
    stop_server
else
    test
fi  
