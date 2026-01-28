[![Docker Image Latest Badge](https://ghcr-badge.egpl.dev/sfu-dhil/digital-mary/latest_tag?trim=major&label=latest)](https://github.com/sfu-dhil/digital-mary/pkgs/container/digital-mary)
[![Docker Image Size badge](https://ghcr-badge.egpl.dev/sfu-dhil/digital-mary/size)](https://github.com/sfu-dhil/digital-mary/pkgs/container/digital-mary)

# Digital Mary

[Digital Mary](digital-mary.dhil.lib.sfu.ca) (affectionately known as DM) is a Python application written using the [Django](https://www.djangoproject.com/) framework. It is a digital tool for collecting and disseminating images of artifacts relating to the Virgin Mary.

## Requirements

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Initialize the Application

    docker compose up -d --build

Frontend will be available at `http://localhost:8080/`
Admin Interface will be available at `http://localhost:8080/admin/`

### Install/Switch the admin theme

    # Bootstrap
    docker exec -it digital_mary_app python manage.py loaddata admin_interface_theme_bootstrap.json

    # Django
    docker exec -it digital_mary_app python manage.py loaddata  admin_interface_theme_django.json

    # Foundation
    docker exec -it digital_mary_app python manage.py loaddata  admin_interface_theme_foundation.json

    # U.S. Web Design Standards
    docker exec -it digital_mary_app python manage.py loaddata  admin_interface_theme_uswds.json

### Create your superuser

    docker exec -it digital_mary_app python manage.py createsuperuser

Enter `username`, `email`, and `password` as prompted

example:

    docker exec -it digital_mary_app python manage.py createsuperuser --username="admin" --email="dhil@sfu.ca"


## General Usage

### Starting the Application

    docker compose up -d

### Stopping the Application

    docker compose down

### Rebuilding the Application (after upstream or js/python package changes)

    docker compose up -d --build

### Viewing logs (each container)

    docker logs -f digital_mary_app
    docker logs -f digital_mary_nginx
    docker logs -f digital_mary_db
    docker logs -f digital_mary_mail

### Accessing the Application

    http://localhost:8080/

### Accessing the Database

Command line:

    PGPASSWORD=password docker exec -it digital_mary_db psql --username=digital_mary digital_mary

Through a database management tool:
- Host:`127.0.0.1`
- Port: `15432`
- Username: `digital_mary`
- Password: `password`

### Accessing Mailhog (catches emails sent by the app)

    http://localhost:8025/

### Database Migrations

Migrate up to latest

    docker exec -it digital_mary_app python manage.py migrate

Create new migrations

    docker exec -it digital_mary_app python manage.py makemigrations

## Updating Application Dependencies

### Yarn (javascript)

    # add new package
    docker exec -it digital_mary_vite yarn add [package]

    # update a package
    docker exec -it digital_mary_vite yarn upgrade [package]

    # update all packages
    docker exec -it digital_mary_vite yarn upgrade

After you update a dependency make sure to rebuild the images

    docker compose down
    docker compose up -d --build

### Pip (python)

Manage python dependencies in `requirements.txt`
>All packages should be locked to a specific version number if possible (Ex `Django==4.2.7`)
>Some special packages cannot be locked and should be noted as such (Ex `psycopg[binary]`)

After making changes, you need to run pip or rebuild the image

    docker exec -it digital_mary_app pip install -r requirements.txt
    # or
    docker compose up -d --build

#### Update a package

Edit version number in `requirements.txt` with new locked version number
>Ex `pip==24.0.0`

    docker exec -it digital_mary_app pip install -r requirements.txt
    # or
    docker compose up -d --build

## Upgrade Postgres Docker version

First turn off everything

    docker compose down

Then backup the postgres data folder

    cp -R .data/postgres .data/postgres-backup

Setup the new version dir

    sudo mkdir -p .data/postgres/<NEW POSTGRES VERSION>/docker
    sudo chown 999:999 -R .data/postgres/<NEW POSTGRES VERSION>
    # example:
    sudo mkdir -p .data/postgres/18/docker
    sudo chown 999:999 -R .data/postgres/18


Using `https://github.com/tianon/docker-postgres-upgrade` to upgrade the postgres version

    docker run --rm \
        --volume .data/postgres:/var/lib/postgresql \
        --env PGDATAOLD=/var/lib/postgresql/<OLD POSTGRES VERSION>/docker \
        --env PGDATANEW=/var/lib/postgresql/<NEW POSTGRES VERSION>/docker \
        --env POSTGRES_USER=digital_mary \
        --env POSTGRES_PASSWORD=password \
        tianon/postgres-upgrade:<OLD POSTGRES VERSION>-to-<NEW POSTGRES VERSION> \
        --link

example:

    docker run --rm \
        --volume .data/postgres:/var/lib/postgresql \
        --env PGDATAOLD=/var/lib/postgresql/17/docker \
        --env PGDATANEW=/var/lib/postgresql/18/docker \
        --env POSTGRES_USER=digital_mary \
        --env POSTGRES_PASSWORD=password \
        tianon/postgres-upgrade:17-to-18 \
        --link
