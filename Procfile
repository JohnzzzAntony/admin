web: mkdir -p staticfiles && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn jkr.wsgi:application --log-file -
