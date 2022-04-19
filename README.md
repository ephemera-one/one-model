# ONE Model

## Dev

1. Run DB and Redis: `docker-compose up -d`
2. Activate env: `source ./env/bin/activate.fish`
3. Running server: `cd src && python manage.py migrate && python manage.py runserver`
4. Running Celery worker: `cd src && celery -A one_model worker`
