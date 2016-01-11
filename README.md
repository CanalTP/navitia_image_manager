

# Docker Image Manager

A set of convenience classes and utilies for abstracting
and automating the creation, run and management of Docker images and containers.
This is oriented for the creation of monolithic docker images (opposite to the usual
microservices view)


## DIM: Docker Image Manager classes

A set of classes to create new docker images out of:

 - a base image or a base Dockerfile that can be inline or file
 - Dockerfiles addons (for apache, postgresql, user, ...)
 - Dockerfile parameters (ports and volumes)
 - Different configuration files

### class DockerRunParameters

Derived from Python dict, this class manges docker run parameters, especially ports, volumes and links.

### class DockerFile

Allows to create a build context together with complex Dockerfile and associated files.

### class DockerImageManager

Allows to create and manage docker images.

### class DockerContainerManager

Allows to manage docker containers.


## FFD: Fabric for Docker

A class and a set of platforms that allows the deployment of Navitia on a Docker image via Fabric scripts.


## Factories

A set of scripts that automates the creation of images, or anything else regarding docker images and containers (running, deleting, ...)

 - navitia_simple.py: create a monolithic Navitia image with a single 'default' coverage.
 - navitia_artemis.py: create an Artemis image for running artemis tests.

You can run any of these scripts with option '--help' for help on the available options.


## Installation

Get the source and install requirements:

    git clone https@github.com:CanalTP/navitia_image_manager.git
    cd navitia_image_manager; pip install -r requirements.txt

You will need Navitia's deployment project too (in the same virtualenv):

    git clone https@github.com:CanalTP/fabric_navitia.git
    cd fabric_navitia; pip install -r requirements.txt

Go to navitia_image_manager/external_images/rabbitmq and build a docker image for rabbitmq:

   docker build -t rabbitmq:latest .
  
----------


## Build a custom Debian8 image

You will need a recent version of docker (1.6 is too old, 1.9 works).
Cd to the root of navitia_image_manager project, then run:

    python factories/navitia_debian8.py

This will build a custom Debian8 image with a set of add-ons (sshd, postgresql, apache...) and a configured supervisord starter for all of them.

Other images (like Artemis) are built upon this image. A 2 stages build process saves time.

----------


## Deploy and run Artemis on Docker



The project provides all the necessary stuff to build and run a complete Artemis platform on any local computer with a minimum set of requirements (at least Debian8 or Ubuntu14).

Features:

 - Artemis code and data is shared between host and docker image,
   allowing short edition - test cycles using host IDE and tools.
 - The database is held in a separate docker image, allowing to save any
   db state for convenience or test purpose.

### Build all the necessary images

Artemis is run in docker using docker compose. Several images are needed for this

#### Artemis

`cd factories/artemis`

`docker build -t navitia/debian8_artemis .`

#### Artemis Database

`cd factories/postgis`

`docker build -t navitia/artemis_db .`

#### Kirin

Clone kirin project (https://github.com/CanalTP/kirin), got the root of the project and build a docker 
image for kirin by running:

    docker build -t kirin:latest .

Clone docker_kirin project (https://github.com/CanalTP/docker_kirin) and build a docker image for 
kirin_config (in the directory `artemis`):

    
    docker build -t kirin_config:artemis . 

### Run all the containers

At this point, check with `docker images` that you should have following images:
    
    rabbitmq:latest
    navitia/artemis
    navitia/artemis_db
    kirin_conifg
    kirin:latest


Cd to navitia_image_manager/docker_compose/artemis and create a docker-compose-configuration.yml with the 
proper paths for artemis/source and artemis/data with absolute path:

```
echo '# own custom pathes
artemis:
  volumes:
   - /home/antoine/dev/artemis:/artemis/source
   - /home/antoine/dev/data_artemis:/artemis/data
   - /home/antoine/dev/reference_artemis:/artemis/references

'> docker_compose/artemis/docker-compose-configuration.yml
```

Run:

  `docker-compose -f docker-compose-artemis.yml -f docker-compose-configuration.yml -f docker-compose-kirin.yml --x-networking up [-d]`
    
It should starts all the differents container.

if you ran it without the `-d` option, you can stop all container by pressing `ctrl+c`.

to remove all container:

  `docker-compose -f docker-compose-artemis.yml -f docker-compose-configuration.yml -f docker-compose-kirin.yml --x-networking rm -f`

### Install navitia

The first time you pop all the different container, you need to install navitia from scratch.

#### Get some navitia packages 
you can build some, or get some from ci.navitia.io. Take care to get some packages build for the artemis 
platform (debian 8).

To get the latest navitia dev branch packages do:

`wget --no-check-certificate https://ci.navitia.io/job/navitia_dev_multi_os/LINUX_DISTRIB=debian8/lastSuccessfulBuild/artifact/\*zip\*/archive.zip`

The packages must be unziped and stored in a different directory.

#### First install
You need fabric ((https://github.com/CanalTP/fabric_navitia)) to install navitia.

Go to the directory with the navitia packages and install navitia with fabric 

* In the python path you need to give the path to the `navitia_image_manager/platforms` dir
* with the -f argument give the path to the fabfile directory of fabric

`PYTHONPATH=../platforms fab -f ../../fabric_navitia/fabfile  use:artemis deploy_from_scratch`

#### Upgrade version

Same as in the first install, but you can call the `upgrade_version` target instead of `deploy_from_scratch`:

`PYTHONPATH=../platforms fab -f ../../fabric_navitia/fabfile  use:artemis upgrade_version`

#### Commit the container
To avoid doing again the whole fabric install, you can commit your navitia container (the containers must 
be stopped):

`docker commit artemis_db navitia/artemis_db`

`docker commit artemis navitia/debian8_artemis`

### Running the tests
Now you can reconnect to artemis and run:

    `docker exec -it artemis bash`
    `CONFIG_FILE=/artemis/source/artemis/default_settings_docker.py python -m py.test artemis/tests`

