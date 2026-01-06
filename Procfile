web: gunicorn lms_platform.wsgi:application --bind 0.0.0.0:$PORT --workers 3 --threads 2 --timeout 120 --log-file - --access-logfile - --error-logfile - --log-level info
