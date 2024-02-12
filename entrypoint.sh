#!/bin/bash
set -e  # Exit on error

# change directory to project directory
cd project/

# # Apply collectstatic
# python manage.py collectstatic --no-input

# Start project
python -m gunicorn scraper.wsgi:application --bind 0.0.0.0:8000 -w 4 --timeout 3600

exec "$@"