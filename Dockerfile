FROM python:3.8.3-buster

RUN apt update

RUN pip install flask && \
    pip install flask_restful && \
    pip install beautifulsoup4 && \
    pip install pymongo && \
    pip install requests && \
    pip install line-bot-sdk

RUN mkdir /var/flask

COPY ./app.py /var/flask
COPY ./lineai.py /var/flask
COPY ./linesticker.py /var/flask
COPY ./push.py /var/flask

EXPOSE "port番号"

ENTRYPOINT ["/usr/local/bin/python", "/var/flask/app.py"]
