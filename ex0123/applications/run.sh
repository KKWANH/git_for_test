gunicorn -c gunicorn.conf.py ex01.wsgi
python3 manage.py makemigrations && python3 manage.py migrate && python3 manage.py runserver