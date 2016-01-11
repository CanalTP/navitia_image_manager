FROM debian:8

# systemd is removed and sysvinit is installed instead.
# As of may 2015, systemd is difficult to launch in a docker container, see http://developerblog.redhat.com/2014/05/05/running-systemd-within-docker-container/
# and if systemd is installed, some packages try to launch via systemctl (eg PostgreSQL) and fail
RUN apt-get update
RUN apt-get install -y sysvinit-core locales sudo
RUN apt-get install -y vim
RUN apt-get remove -y systemd

RUN apt-get install -y  postgresql-server-dev-all postgis

# change configuration to accept untrusted connections from remote hosts
RUN echo 'host  all  all  0.0.0.0/0  password' >> /etc/postgresql/9.4/main/pg_hba.conf
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.4/main/postgresql.conf

#little tunning of postgres to speed up things
RUN sed -i 's/#\?shared_buffers = [0-9]*MB/shared_buffers = 2048MB/' /etc/postgresql/9.4/main/postgresql.conf
RUN sed -i 's/#\?work_mem = [0-9]*MB/work_mem = 16MB/' /etc/postgresql/9.4/main/postgresql.conf
RUN sed -i 's/#\?checkpoint_segments = [0-9]*/checkpoint_segments = 30/' /etc/postgresql/9.4/main/postgresql.conf

# we create the default db:
RUN service postgresql start && \
    /bin/su postgres -c "psql -c \"CREATE USER kirin PASSWORD 'kirin'\"" && \
    /bin/su postgres -c "createdb kirin --owner=kirin --encoding=UTF8 --template=template0" && \
    service postgresql stop

# configure SSH server
RUN apt-get install -y openssh-server
RUN mkdir -p /var/run/sshd

RUN mkdir -p /root/.ssh
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
COPY unsecure_key.pub /root/.ssh/authorized_keys
RUN chmod 644 /root/.ssh/authorized_keys

#configure supervisord
RUN apt-get install -y supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]
