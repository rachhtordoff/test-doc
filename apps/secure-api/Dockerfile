FROM python 3.5.3
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


COPY / /opt/

RUN apt-get install -y libpq-dev

RUN pip3 install -q -r /opt/requirements.txt && \
  pip3 install -q -r /opt/requirements_test.txt

RUN pip3 -q install gunicorn eventlet

EXPOSE 8000

WORKDIR /opt

CMD ["/usr/local/bin/gunicorn", "-k", "eventlet", "--pythonpath", "/opt", "--access-logfile", "-", "manage:manager.app", "--reload", "-b", "0.0.0.0:8000"]
