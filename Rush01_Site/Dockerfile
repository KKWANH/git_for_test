FROM	python:3.9

RUN		mkdir /usr/src/app
WORKDIR		/usr/src/app

ENV		PYTHONUNBUFFERED 1
ENV		PYTHONDONTWRITEBYTECODE 1

COPY		./requirement.txt .
RUN		python -m pip install --upgrade pip
RUN		python -m pip install -r requirement.txt

COPY		. .
