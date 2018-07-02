#!/bin/bash
set -e

if [ "$1" = 'sam-events' ]; then
    exec /app/sam-events
fi

exec "$@"
