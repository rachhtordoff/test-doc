FROM ubuntu:14.04
MAINTAINER Rachael Tordoff

ENV APP_NAME fact-find-api
ENV FLASK_LOG_LEVEL DEBUG
ENV LOG_LEVEL DEBUG
ENV COMMIT LOCAL
ENV PYTHONPATH /opt

ENV SECRET_KEY you-will-never-guess

#database settings
ENV SQLALCHEMY_MIGRATE_REPO '/opt/db_repository'
ENV SQLALCHEMY_USER 'optiself_user'
ENV SQLALCHEMY_PASSWORD 'password'
ENV SQLALCHEMY_HOST 'postgres'
ENV SQLALCHEMY_PORT '5432'
ENV SQLALCHEMY_DB 'optiself_user'

#amazon settings
ENV ACCESS_KEY 'AKIAICXOUOMKVT74IOBA'
ENV aws_SECRET_KEY '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'
COPY / /opt/

RUN apt-get update
RUN apt-get install -y build-essential python3-dev python3-pip

RUN apt-get install -y libpq-dev

RUN pip3 install -q -r /opt/requirements.txt && \
  pip3 install -q -r /opt/requirements_test.txt

RUN pip3 -q install gunicorn eventlet

EXPOSE 8000

WORKDIR /opt

CMD ["/usr/local/bin/gunicorn", "-k", "eventlet", "--pythonpath", "/opt", "--access-logfile", "-", "manage:manager.app", "--reload", "-b", "0.0.0.0:8000"]
