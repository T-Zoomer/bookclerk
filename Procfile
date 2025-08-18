release: mkdir -p /app/data && python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: gunicorn bookclerk_project.wsgi --log-file -