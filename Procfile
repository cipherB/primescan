web: python manage.py makemigrations && python manage.py migrate && gunicorn primascan.wsgi;
heroku config:set DISABLE_COLLECTSTATIC=1