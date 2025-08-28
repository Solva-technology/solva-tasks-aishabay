#!/bin/sh
set -e

alembic upgrade head
uvicorn code.main:app --host 0.0.0.0 --port 8000 --reload

exec "$@"
