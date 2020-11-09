#!/bin/bash

if [ ! -f "./nexus.json" ]; then
    echo "nexus.json file is missing"
    exit 1
fi

base_command="docker-compose -f docker-compose.yaml -f nexus-configure-compose.yaml"

if [ "$#" -eq 0 ]; then
    $base_command up -d --abort-on-container-exit
else
    $base_command $@
fi
