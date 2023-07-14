web: python manage.py migrate && python manage.py collectstatic --no-input && celery -A ExpertCard worker --loglevel=info && gunicorn Expertcard.wsgi:application

