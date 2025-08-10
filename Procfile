web: gunicorn fintech.wsgi --log-file -
worker: celery -A fintech worker --loglevel=info