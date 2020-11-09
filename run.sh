#!/bin/bash
base_command="docker-compose -f docker-compose.yaml"

if [ "$#" -eq 0 ]; then
    `$base_command up -d`
else
    `$base_command $@`
fi
