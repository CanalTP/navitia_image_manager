# encoding: utf-8


def absjoin(*p):
    return os.path.abspath(os.path.join(*p))

import os.path
ROOT = absjoin(__file__, '..', '..', '..')
import sys
sys.path[0] = ROOT

from clingon import clingon

from navitia_docker_manager import utils


@clingon.clize(navitia_folder=('n', 'f'))
def factory(navitia_folder=''):
    sys.stdout.write(utils.get_packet_version(navitia_folder))
