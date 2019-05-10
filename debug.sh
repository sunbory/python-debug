#!/bin/bash
#
ROOT_PATH=$(cd $(dirname "$0") && pwd)

case $1 in
build)
    docker build -f debug/Dockerfile -t python-debugging .
    ;;
start)
    docker run -d --rm -p 3000:3000 -v $(pwd):/opt/ python-debugging
    ;;
stop)
    for id in $(docker ps | awk '/python-debugging/{print $1}'); do
        docker stop ${id}
    done
    ;;
*)    
    while true; do

        python -m ptvsd --host 0.0.0.0 --port 3000 --wait -m py

        sleep 1

    done
    ;;
esac
