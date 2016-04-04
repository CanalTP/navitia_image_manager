FROM debian:8

# systemd is removed and sysvinit is installed instead.
# As of may 2015, systemd is difficult to launch in a docker container, see http://developerblog.redhat.com/2014/05/05/running-systemd-within-docker-container/
# and if systemd is installed, some packages try to launch via systemctl (eg PostgreSQL) and fail
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y sysvinit-core
RUN apt-get install -y python2.7-dev python-pip locales sudo git logrotate vim
RUN apt-get remove -y systemd

RUN pip install --upgrade pip virtualenv

COPY {rabbitmq_config} /etc/rabbitmq/rabbitmq.config
RUN chmod a+r /etc/rabbitmq/rabbitmq.config

CMD ["/bin/bash"]
