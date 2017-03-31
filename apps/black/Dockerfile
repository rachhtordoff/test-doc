FROM ubuntu:14.04
MAINTAINER  Rachael Tordoff

ENV APP_NAME admin-frontend
ENV FLASK_LOG_LEVEL DEBUG
ENV LOG_LEVEL DEBUG
ENV COMMIT LOCAL
ENV PYTHONPATH /opt

ENV SECRET_KEY you-will-never-guess
ENV SECURE_API_URL http://secure_api:8000

#amazon settings
ENV ACCESS_KEY 'AKIAI3IU22QGPH34WHAQ'
ENV SECRET_KEY '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'

COPY / /opt/

RUN apt-get update
RUN apt-get install -y build-essential python3-dev python3-pip

RUN pip3 install -q -r /opt/requirements.txt && \
  pip3 install -q -r /opt/requirements_test.txt

RUN pip3 -q install gunicorn eventlet

EXPOSE 8000

WORKDIR /opt

CMD ["/usr/local/bin/gunicorn", "-k", "eventlet", "--pythonpath", "/opt", "--access-logfile", "-", "manage:manager.app", "--reload", "-b", "0.0.0.0:8000"]
