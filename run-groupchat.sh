#! /usr/bin/env bash

if [ -z $(docker image ls -q groupchat) ]; then
    echo "building..."
    docker build -t groupchat . &> /dev/null
    echo "ready"
    echo ""
fi

docker run -it groupchat
