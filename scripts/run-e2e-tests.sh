#!/bin/bash


echo "Initiating containers"
docker-compose up -d

if [ -z ${PYTHON_VERSION+x} ]; then
    envlist=ALL
else
    envlist=$(echo $PYTHON_VERSION | sed -E 's/([0-9])\./py\1/')
fi

echo "Running tox"
tox -e $envlist -- cognosaurus/api/tests/e2e "$@"

echo "Terminating containers"
docker-compose down
