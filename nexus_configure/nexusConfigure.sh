#!/bin/bash

set -e

python -m pip install requests

while [[ "$(curl -s -o /dev/null -w ''%{http_code}'' localhost:8081)" != "200" ]]; do echo 'Waiting for nexus'; sleep 1; done

PATH=$PATH:/scripts/ python /scripts/nexusConfigure.py /settings/nexus.json