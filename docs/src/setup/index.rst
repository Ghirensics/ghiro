Setup Ghiro
===========

Ghiro is supposed to run on a *GNU/Linux* native system.
For the purpose of this documentation, we chose **latest Ubuntu Server** as
reference system for the commands examples.
Probably Ghiro could work on other systems like MacOSX but this is not tested
and out of scope of this documentation.

Requirements
============

Ghiro has the following requirements:

    * MongoDB: you need to run a MongoDB database (at least release 2.0)
    * Python: that's how we roll (only Python 2.x, at least release 2.7)
    * Python-magic: for MIME extraction
    * Gexiv: for metadata extraction (at least release 0.4)
    * Python Imaging Library (PIL): for image manipulation (at least release 1.1)
    * Python-dateutil: for datetime manipulation
    * Pymongo: driver for MongoDB (at least release 2.5)
    * Django: for web interface (at least release 1.5)

If you choose MySQL or PostgrSQL as database you have to install their additional drivers.

Getting started
===============

Download and extract
--------------------

Download Ghiro as explained in this documentation, if you download the stable
package extract it. Enter in the Ghiro folder.

Requirements
------------

If you don't have already it, install MongoDB with the following command (run as root or with sudo)::

    apt-get install mongodb

Install required libraries with the the following commands (run as root or with sudo)::

    apt-get install python-pip python-magic libgexiv2-1 python-imaging python-dateutil
    apt-get install build-essential python-dev

Install latest Django with the following command (run as root or with sudo)::

    pip install django

Install latest PyMongo with the following command (run as root or with sudo)::

    pip install pymongo

Preparing
---------

The default databases are SQLite3 and MongoDB (you need to have it listening on
localhost). If you need to change this see the configuration chapter below.

First of all you need to create an empty database with the following command
(inside Ghiro's root)::

    python manage.py syncdb

You will be asked to create a superuser for administration, choose *yes* and
fill all the required fields.

Running
-------

To start the web interface run the following command (inside Ghiro's root)::

    python manage runserver

A web server running Ghiro will be available on http://127.0.0.1:8000/
If you need to listen expose Ghiro to all addresses or change the port (in this
example is 9000) run the following command (inside Ghiro's root)::

    python manage runserver 0.0.0.0:9000

To start processing images you have to start the processing deamon, run the
following command (inside Ghiro's root)::

    python manage.py process


Configuration
=============

Ghiro works pretty well with default options, which are SQLite3 as
relational database and use MongoDB installed and listening on local
host.
If you want to change any setting the configuration file is located
in *ghiro/local_settings.py*.
The default settings will fit all common user needs.

Following is the default *ghiro/local_settings.py* file::

    LOCAL_SETTINGS = True
    from settings import *

    DATABASES = {
        'default': {
            # Engine type. Ends with 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'ENGINE': 'django.db.backends.sqlite3',
            # Database name or path to database file if using sqlite3.
            'NAME': 'db.sqlite',
            # Credntials. The following settings are not used with sqlite3.
            'USER': '',
            'PASSWORD': '',
            # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'HOST': '',
            # Set to empty string for default port.
            'PORT': '',
        }
    }

    # MySQL tuning.
    #DATABASE_OPTIONS = {
    # "init_command": "SET storage_engine=INNODB",
    #}

    # Mongo database settings
    MONGO_URI = "mongodb://localhost/"
    MONGO_DB = "ghirodb"

    # Max uploaded image size (in bytes).
    # Default is 150MB.
    MAX_FILE_UPLOAD = 157286400

    # Allowed file types.
    ALLOWED_EXT = ['image/bmp', 'image/x-canon-cr2', 'image/jpeg', 'image/png',
                   'image/x-canon-crw', 'image/x-eps', 'image/x-nikon-nef',
                   'application/postscript', 'image/gif', 'image/x-minolta-mrw',
                   'image/x-olympus-orf', 'image/x-photoshop', 'image/x-fuji-raf',
                   'image/x-panasonic-raw2', 'image/x-tga', 'image/tiff', 'image/pjpeg']

    # Override default secret key stored in secret_key.py
    # Make this unique, and don't share it with anybody.
    # SECRET_KEY = "YOUR_RANDOM_KEY"

    # Language code for this installation. All choices can be found here:
    # http://www.i18nguy.com/unicode/language-identifiers.html
    LANGUAGE_CODE = "en-us"

    ADMINS = (
        # ("Your Name", "your_email@example.com"),
    )

    MANAGERS = ADMINS

    # Allow verbose debug error message in case of application fault.
    # It's strongly suggested to set it to False if you are serving the
    # web application from a web server front-end (i.e. Apache).
    DEBUG = True

    # A list of strings representing the host/domain names that this Django site
    # can serve.
    # Values in this list can be fully qualified names (e.g. 'www.example.com').
    # When DEBUG is True or when running tests, host validation is disabled; any
    # host will be accepted. Thus it's usually only necessary to set it in production.
    ALLOWED_HOSTS = ["*"]

If you change the configuration after the first setup, before editing this file you have to stop both Ghiro's web interface and
processing deamon, you may restart them after the edit.

If you changed any setting related to the database configuration you have to
re-build your database with the command (inside Ghiro's root)::

    python manage.py syncdb

Running Ghiro as service
========================

If you want to run Ghiro as an enterprise service you have to get rid of Django web server and run
Ghiro with a production ready tool.

Database
--------
We do not suggest SQLite3 for production environment, please go for MySQL or PostgreSQL.
In this example we are going to show you how to configure Ghiro with MySQL.

Setup MySQL and Python drivers with the following command (run as root or with sudo)::

    apt-get install mysql-server python-mysqldb

Go through the wizard and set MySQL password.
Configure Ghiro to use MySQL as explained in configuration paragraph.

Apache as a front-end
---------------------

Now we are going to configure Apache as a front end for Ghiro's django application.

Setup Apache and mod_wsgi with the following command (run as root or with sudo)::

    apt-get install apache2 libapache2-mod-wsgi