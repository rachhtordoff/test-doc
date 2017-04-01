FROM ubuntu:14.04
MAINTAINER Chris Brantley

RUN apt-get update

COPY nginx.conf /etc/nginx/nginx.conf
COPY runserver.sh /

RUN chmod a+x /runserver.sh

EXPOSE 80
CMD ["/runserver.sh"]
