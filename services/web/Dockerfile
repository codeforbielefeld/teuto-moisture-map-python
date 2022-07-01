# Based on: https://runnable.com/docker/python/dockerize-your-flask-application
FROM python:3.8

WORKDIR /usr/src/app

COPY src/requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY src /usr/src/app

WORKDIR /usr/src/app

ENV FLASK_ENV=development

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
