#!/bin/bash

case $1 in
Start)
    docker run -d --rm -p 3000:3000 -v $(pwd):/opt/ remote-debugging-docker
    ;;
Stop)
    for id in $(docker ps | awk '/remote-debugging-docker/{print $1}'); do
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
