#!/bin/sh
set -e

alembic -c services/core/alembic.ini upgrade head
uvicorn services.core.code.main:app --host 0.0.0.0 --port 8000 --reload

exec "$@"
