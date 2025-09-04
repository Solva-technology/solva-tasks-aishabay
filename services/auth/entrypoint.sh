#!/bin/sh
set -e

alembic -c services/auth/alembic.ini upgrade head
uvicorn services.auth.code.main:app --host 0.0.0.0 --port 8000 --reload

exec "$@"
