#!/bin/bash

source /usr/local/bin/virtualenvwrapper.sh

LOGFILE=/var/log/gunicorn/nearu.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=5
workon nearuEnv

test -d $LOGDIR || mkdir -p $LOGDIR

exec gunicorn pymongoserver.wsgi:application -b 0.0.0.0:8000 -w 4 --log-level=debug --log-file=/var/log/gunicorn/nearu.log 2>>/var/log/gunicorn/nearu.log

# lsof -i:8080 -n