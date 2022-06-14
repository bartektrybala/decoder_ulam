
#!/bin/bash

python manage.py collectstatic --no-input

python manage.py migrate --no-input

gunicorn weirdtext.wsgi:application --bind 0.0.0.0:8000
