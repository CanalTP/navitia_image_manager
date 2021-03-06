# encoding: utf-8

from __future__ import unicode_literals, print_function
import subprocess

from fabric.api import env
from fabfile.instance import add_instance
from common import env_common

POSTGIS_HOST = 'artemis_db'


def get_docker_ip(docker_name):
    return eval(subprocess.check_output(["docker", "inspect", "--format",
                                         "'{{ .NetworkSettings.Networks.artemis.IPAddress }}'",
                                         docker_name]))


def artemis(_=None):
    host = 'root@' + get_docker_ip('artemis')
    db = 'root@' + get_docker_ip(POSTGIS_HOST)

    env_common(host, db, host, host)
    env.name = 'artemis'
    env.postgresql_database_host = POSTGIS_HOST

    env.rabbitmq_host = 'rabbitmq'

    env.jormungandr_additional_settings['CIRCUIT_BREAKER_MAX_FAIL'] = 10
    env.jormungandr_additional_settings['CIRCUIT_BREAKER_TIMEOUT_S'] = 1

    add_instance("corr-02", "corr-02")
    add_instance("airport-01", "airport-01")
    add_instance("prolong-mano", "prolong-mano")
    add_instance("bibus", "bibus")
    add_instance("mission", "mission")
    add_instance("test-02", "test-02")
    add_instance("sherbrooke", "sherbrooke")
    add_instance("stif", "stif")
    add_instance("test-03", "test-03")
    add_instance("nb-corr-05", "nb-corr-05")
    add_instance("rebroussement", "rebroussement")
    add_instance("map", "map")
    add_instance("fr-pdl", "fr-pdl")
    add_instance("nb-corr-04", "nb-corr-04")
    add_instance("freqgtfs", "freqgtfs")
    add_instance("corr-01", "corr-01")
    add_instance("passe-minuit-01", "passe-minuit-01")
    add_instance("guichet-unique", "guichet-unique", enable_realtime=True, rt_topics=['realtime.ire'])
    add_instance("freqparis", "freqparis")
    add_instance("itl", "itl")
    add_instance("poitiers", "poitiers")
    add_instance("test-01", "test-01")
    add_instance("boucle-01", "boucle-01")
    add_instance("paysdelaloire", "paysdelaloire")
    add_instance("saintomer", "saintomer")
    add_instance("airport", "airport")
    add_instance("tcl", "tcl")
    add_instance("passe-minuit-02", "passe-minuit-02")
    add_instance("nb-corr-01", "nb-corr-01")
    add_instance("mdi", "mdi")
    add_instance("nb-corr-03", "nb-corr-03")
    add_instance("prolong-auto", "prolong-auto")
    add_instance("nb-corr-02", "nb-corr-02")
    add_instance("freqsimple", "freqsimple")
    add_instance("freqgtfs-01", "freqgtfs-01")
    add_instance("tad", "tad")
    add_instance("fr-auv", "fr-auv")

