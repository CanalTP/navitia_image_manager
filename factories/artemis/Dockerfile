FROM navitia/debian8:latest

RUN pip install pytest

RUN mkdir -m 777 -p /srv/ed/data

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY kraken_service_wrapper /usr/local/bin/kraken_service_wrapper
RUN chmod a+x /usr/local/bin/kraken_service_wrapper

RUN apt-get install -y openssh-server
# configure SSH server
RUN mkdir -p /var/run/sshd

RUN mkdir -p /root/.ssh
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd
COPY unsecure_key.pub /root/.ssh/authorized_keys
RUN chmod 644 /root/.ssh/authorized_keys

RUN apt install -y vim

# for artemis we'll need a virtualenv to install the requirements
RUN apt-get update
RUN apt-get install -y python-dev
RUN pip install virtualenvwrapper
RUN /bin/bash -c "source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv artemis"
COPY launch_artemis.sh /launch_artemis.sh
RUN chmod a+x /launch_artemis.sh
