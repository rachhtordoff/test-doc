FROM python:3.5.3
MAINTAINER Rachael Tordoff

ENV APP_NAME client-frontend
ENV FLASK_LOG_LEVEL DEBUG
ENV LOG_LEVEL DEBUG
ENV COMMIT LOCAL
ENV PYTHONPATH /opt

ENV SECRET_KEY you-will-never-guess
ENV SECURE_API_URL http://secure_api:8000

COPY / /opt/

RUN pip3 install -q -r /opt/requirements.txt

RUN pip3 -q install gunicorn eventlet

EXPOSE 8000

WORKDIR /opt

CMD ["/usr/local/bin/gunicorn", "-k", "eventlet", "--pythonpath", "/opt", "--access-logfile", "-", "manage:manager.app", "--reload", "-b", "0.0.0.0:8000"]
