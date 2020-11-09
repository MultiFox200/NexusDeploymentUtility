#!/bin/bash
base_command="docker-compose"

if [ "$#" -eq 0 ]; then
    $base_command up -d
else
    $base_command $@
fi
