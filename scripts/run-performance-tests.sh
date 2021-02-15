#!/bin/bash


no_db_test() {
    tox -e "$envlist-performance" -- cognosaurus/api/tests/performance/test_api_without_db.py -s "$@"
}

db_test() {
    # dump.rdb is in redis/
    cd redis/
    echo "Initiating redis"
    redis-server --port $REDIS_PORT --daemonize yes
    cd ..

    tox -e $envlist -- cognosaurus/api/tests/performance/test_api_with_db.py -s "$@"

    echo "Terminating redis"
    redis-cli -p $REDIS_PORT shutdown nosave
}

REDIS_HOST=0.0.0.0
REDIS_PORT=3000

if [ -z ${PYTHON_VERSION+x} ]; then
    envlist="py36"
else
    envlist=$(echo $PYTHON_VERSION | sed -E 's/([0-9])\./py\1/')
fi

flag=$1
shift
echo "Running tox"
if [ $flag == "--db=yes" ]; then
    db_test
elif [ $flag == "--db=no" ]; then
    no_db_test
else
    db_test
    no_db_test
fi
