

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

The project provides all the necessary stuff to build and run a complete Artemis platform on any local computer with a minimum set of requirements (at least Debian8 or Ubuntu14, 16 GB RAM).

Features:

 - Artemis code and data is shared between host and docker image,
   allowing short edition - test cycles using host IDE and tools.
 - The database is held in a separate docker image, allowing to save any
   db state for convenience or test purpose.

### Create and start the Postgres/Postgis container

Cd to the root of navitia_image_manager project, then run:

    python factories/navitia_postgis.py

This will build and start a posgres/postgis image based on a Debian8. A "cities" database will also be added, ready to be populated. The image is named navitia/postgis, the container is named postgis.

Then restart postgresql:

    docker exec -it artemis_db /usr/sbin/service postgresql restart

Your docker container for postgres/posgis is ready but it is still empty (except an empty "cities" database).
The next steps, while creating a Navitia image, will also create other Navitia databases and populate the cities db.

### Create and start the Artemis image

Cd to the root of navitia_image_manager project, then run:

    PYTHONPATH=/home/francois/CanalTP/fabric_navitia python factories/navitia_artemis.py -n /path/to/navitia/packages -v yes -r -t -c

This will build and commit a new Navitia image explicitely targetted for Artemis.

> Warning 1: the postgis docker container must be started prior to launching this command.

> Warning 2: use Navitia packages built for the appropriate distribution (currently Debian8).

Run this image:

    docker run -d -p 8080:80 -v /path/to/artemis_data:/artemis/data -v /path/to/artemis:/artemis/source --link artemis_db --name artemis navitia/debian8_artemis

Then connect to it:

    docker exec -it artemis /bin/bash

### Prepare the cities database

Once connected to the Artemis container, cd to cities' alembic folder:

    cd /usr/share/navitia/cities/alembic

then replace the file alembic.ini with the one found in project navitia_image_manager, at path factories/artemis/alembic.ini (TODO: automate this), then run the alembic process to create the database schema:

    alembic -c alembic.ini upgrade head

From your host, place a france-latest.osm.pbf file into the /path/to/artemis_data folder (shared folder), then launch the cities command in the container:

    cities -i /artemis/data/france-latest.osm.pbf --connection-string 'user=cities password=cities host=artemis_db port=5432 dbname=cities'

Running this command requires at least 16GB of RAM. Once the cities database is populated, you want to save your work. Disconnect from artemis image and commit the Postgis container:

    docker stop artemis_db && docker commit artemis_db navitia/artemis_db

Then run it again:

    docker rm -v artemis_db && docker run -d --name artemis_db  navitia/artemis_db

Alternatively, a docker-compose.yml model is provided to start Artemis with Postgis as a dependancy (link).

### Launch Artemis tests

Connect to artemis container and cd to /artemis/source, then run (you might need to grant write access to the /artemis/data/ sub-directories to www-data) :

    CONFIG_FILE=/artemis/source/artemis/default_settings_docker.py python -m py.test artemis/tests

### Launch Kirin tests

Clone kirin project, got the root of the project and build a docker image for kirin by running:

    docker build -t kirin:latest .

Clone docker_kirin project and build a docker image for kirin_config:

    docker build -t kirin_config:artemis . 

At this point, check with `docker images` that you should have following images:
    
    rabbitmq:latest
    navitia/artemis
    navitia/artemis_db
    kirin_conifg
    kirin:latest

Cd to navitia_image_manager/docker_compose/artemis, open docker-compose-artemis-volumes.yml and give the proper paths for
artemis/source and artemis/data with absolute path.

Run:
  docker-compose -f docker-compose-artemis.yml -f docker-compose-artemis-volumes.yml -f docker-compose-kirin.yml --x-networking up [-d]
    
Now you can reconnect to artemis and run:

    CONFIG_FILE=/artemis/source/artemis/default_settings_docker.py python -m py.test artemis/tests

