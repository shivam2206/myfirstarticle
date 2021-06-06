#!/bin/sh

# Wait for the DB to be ready
sleep 30s
flask db upgrade || exit 1
gunicorn app:app --bind 0.0.0.0:5000

