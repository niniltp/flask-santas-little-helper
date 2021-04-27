FROM python:3.9.2-alpine

ENV STATIC_INDEX 1

WORKDIR /root

RUN apk add gcc build-base linux-headers libffi-dev freetype-dev libjpeg-turbo-dev zlib-dev

ADD . /root

RUN pip3 install -r requirements.txt
RUN chmod +x db_init.sh

ENV FLASK_LIVERELOAD=False

RUN ./db_init.sh

ENTRYPOINT flask run --host=0.0.0.0


