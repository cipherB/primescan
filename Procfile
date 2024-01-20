heroku buildpacks:add --index 1 heroku/python
heroku buildpacks:add --index 2 https://github.com/heroku/heroku-buildpack-apt.git
web: python manage.py makemigrations && python manage.py migrate && gunicorn primascan.wsgi;
heroku config:set DISABLE_COLLECTSTATIC=1