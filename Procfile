web: mkdir -p staticfiles && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn jkr.wsgi:application --bind 0.0.0.0:$PORT --log-file -
