#!/bin/bash
set -e

superset db upgrade
superset fab create-admin --username "$ADMIN_USERNAME" --firstname Admin --lastname User --email "$ADMIN_EMAIL" --password "$ADMIN_PASSWORD" || true
superset init

echo "Superset init complete."
echo "Create connection: Name: DORIEH (case sensitive); URL: postgresql+psycopg2://dorieh:dorieh_secret@postgres:5432/dorieh2"
