#!/bin/sh
# If some arguments are provided they are just given as is to pytest
# else launch all artemis tests

if [ "$#" -ne 0 ]; then
additional_args=$@
else
additional_args=/artemis/source/artemis
fi

source /usr/local/bin/virtualenvwrapper.sh

workon artemis

pip install -r /artemis/source/requirements.txt

CONFIG_FILE=/artemis/source/artemis/default_settings_docker.py python -m py.test $additional_args
