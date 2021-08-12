#참고: 기존 세팅된 모든 비밀번호는 0987qwer이다

# pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver