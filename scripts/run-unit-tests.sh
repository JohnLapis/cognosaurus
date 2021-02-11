#!/bin/bash


REDIS_HOST=0.0.0.0
REDIS_PORT=3000

echo "Initiating redis"
redis-server --port $REDIS_PORT --daemonize yes

if [ -z ${PYTHON_VERSION+x} ]; then
    envlist=ALL
else
    envlist=$(echo $PYTHON_VERSION | sed -E 's/([0-9])\./py\1/')
fi

echo "Running tox"
tox -e $envlist -- cognosaurus/api/tests/unit/ "$@"

echo "Terminating redis"
redis-cli -p $REDIS_PORT shutdown nosave
