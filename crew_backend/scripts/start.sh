#! /usr/bin/env sh
set -e

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
LOG_LEVEL=${LOG_LEVEL:-info}

if [ $APP_ENV = "dev" ]; then
    exec uvicorn --reload --host $HOST --port $PORT \
        --log-level $LOG_LEVEL crew_backend.main:app
else
    exec gunicorn crew_backend.main:app --workers 2 \
        --worker-class uvicorn.workers.UvicornWorker --bind $HOST:$PORT
fi