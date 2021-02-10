#!/bin/bash


REDIS_PORT=3000

# dump.rdb is in redis/
cd redis/
echo "Initiating redis"
redis-server --port $REDIS_PORT --daemonize yes
cd ..

echo "Running tox"
tox -- cognosaurus/api/tests/integration/ "$@"

echo "Terminating redis"
redis-cli -p $REDIS_PORT shutdown nosave
