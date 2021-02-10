#!/bin/bash


echo "Initiating containers"
docker-compose up -d

echo "Running tox"
tox -- cognosaurus/api/tests/e2e "$@"

echo "Terminating containers"
docker-compose down
