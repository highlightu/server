FROM python:3.7
MAINTAINER ajs7270@naver.com

RUN apt-get -y update && apt-get -y -qq install\
	git \
	libsm6 \
	libxext6 \
	libxrender1 \
	ffmpeg 

# copy source code
COPY . /usr/src/app

# python package install
WORKDIR /usr/src/app
RUN 	pip install -r requirements.txt

# database migrate
RUN 	python manage.py makemigrations \
	&& python manage.py migrate

# run server
EXPOSE 	80
CMD	python manage.py runserver 0.0.0.0:80


