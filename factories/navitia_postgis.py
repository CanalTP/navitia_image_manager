# encoding: utf-8


def absjoin(*p):
    return os.path.abspath(os.path.join(*p))

import os.path
ROOT = absjoin(__file__, '..', '..', '..')
import sys
import time
sys.path[0] = ROOT

from clingon import clingon
clingon.DEBUG = True

from navitia_image_manager import DIM


IMAGE_NAME = 'navitia/postgis'
CONTAINER_NAME = 'postgis'


@clingon.clize
def factory(commit=False):
    df = DIM.DockerFile(
        'factories/postgis/Dockerfile',
        'factories/postgis/supervisord.conf',
        'ssh/unsecure_key.pub',
        add_ons=('sshserver', 'supervisor', ),
        template_context=dict(home_ssh='/root/.ssh')
    )
    dim = DIM.DockerImageManager(df, image_name=IMAGE_NAME, parameters=drp)
    dim.build()
    dcm = dim.create_container(CONTAINER_NAME, start=True, if_exist='remove')
    time.sleep(3)
    dcm.exec_container('sudo -u postgres psql -c "CREATE USER cities PASSWORD \'cities\'"')
    dcm.exec_container('sudo -u postgres createdb cities --owner=cities --encoding=UTF8 --template=template0')
    dcm.exec_container('sudo -u postgres psql -c "CREATE EXTENSION postgis" --dbname=cities')
    if commit:
        dcm.stop()
        dcm.commit(IMAGE_NAME)
        dcm.remove_container()
