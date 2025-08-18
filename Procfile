release: uv run python manage.py migrate --noinput && uv run python manage.py collectstatic --noinput
web: uv run gunicorn bookclerk_project.wsgi --log-file -