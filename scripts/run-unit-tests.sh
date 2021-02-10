#!/bin/bash


REDIS_HOST=0.0.0.0
REDIS_PORT=3000

echo "Initiating redis"
redis-server --port $REDIS_PORT --daemonize yes

echo "Running tox"
tox -- cognosaurus/api/tests/unit/ "$@"

echo "Terminating redis"
redis-cli -p $REDIS_PORT shutdown nosave
