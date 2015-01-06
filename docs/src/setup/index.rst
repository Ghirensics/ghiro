Setup Ghiro
===========

Ghiro is supposed to run on a *GNU/Linux* native system.
For the purpose of this documentation, we choose **latest Ubuntu LTS Server** as
reference system for the commands examples, although Ghiro works on any
GNU/Linux distribution.
Probably Ghiro could work on other systems like MacOSX but this is not tested
and out of scope of this documentation.

Requirements
============

Ghiro has the following requirements:

    * MongoDB: you need to run a MongoDB database (at least release 2.0)
    * Python: that's how we roll (only Python 2.x, at least release 2.7)
    * Python-magic: for MIME extraction
    * Python 2.x bindings for gobject-introspection libraries, required by Gexiv2
    * Gexiv2: for metadata extraction (at least release 0.6.1)
    * Pillow (Python Imaging library - PIL fork): for image manipulation
    * Python-dateutil: for datetime manipulation
    * Pymongo: driver for MongoDB (at least release 2.5)
    * Django: for web interface (at least release 1.5, suggested django 1.6.x)
    * Chardet: for text encoding detection
    * Pdfkit: used for PDF report generation (at least release 0.4)
    * Wkhtmltopdf: used by pdfkit

If you choose MySQL or PostgrSQL as database you have to install their additional drivers.

Ghiro web application is tested and working on the following browsers:

    * Internet Explorer 8, Internet Explorer 9, Internet Explorer 10
    * Mozilla Firefox 24
    * Opera 17
    * Safari 7
    * IOS 7 for Ipad and Iphone

Getting started
===============

Download and extract
--------------------

Download Ghiro as explained in this documentation, if you download the stable
package extract it. Enter in the Ghiro folder.

Preparing
---------

If you don't have already it, install MongoDB with the following command
(run as root or with sudo)::

    apt-get install mongodb

Ghiro works with SQLite although it is strongly suggested to use MySQL or PostgreSQL
as database. If SQLite is used, Ghiro will automatically decrease processing
pallellism to one because SQLite does not support concurrent operations.
Optionally, as an example, you can install MySQL with the following command
(run as root or with sudo)::

    apt-get install mysql-server

Install required libraries with the following commands
(run as root or with sudo)::

    apt-get install python-pip build-essential python-dev python-gi
    apt-get install libgexiv2-2 gir1.2-gexiv2-0.10 wkhtmltopdf
    apt-get install libtiff4-dev libjpeg8-dev zlib1g-dev libfreetype6-dev
    apt-get install liblcms2-dev libwebp-dev tcl8.5-dev tk8.5-dev python-tk


The wkhtmltopdf tool used for PDF report generation needs a X server running, if
you don't have one just install XFVB and configure wkhtmltopdf to use it with::

    apt-get install xvfb
    printf '#!/bin/bash\nxvfb-run --server-args="-screen 0, 1024x768x24" /usr/bin/wkhtmltopdf $*' > /usr/bin/wkhtmltopdf.sh
    chmod a+x /usr/bin/wkhtmltopdf.sh
    ln -s /usr/bin/wkhtmltopdf.sh /usr/local/bin/wkhtmltopdf

Install updated libraries via pip with the following commands
(run as root or with sudo)::

    pip install -r requirements.txt

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

Following is the default *ghiro/local_settings.py* file:

.. literalinclude:: ../../../ghiro/local_settings.py

If you change the configuration after the first setup, before editing this file
you have to stop both Ghiro's web interface and processing deamon, you may
restart them after the edit.

If you changed any setting related to the database configuration you have to
re-build your database with the command (inside Ghiro's root)::

    python manage.py syncdb

Running Ghiro as service
========================

If you want to run Ghiro as a service you have to get rid of Django web server
and run Ghiro inside a web server (i.e. Apache).

Database
--------
We do not suggest SQLite3 for production environment, please go for MySQL or
PostgreSQL.
In this example we are going to show you how to configure Ghiro with MySQL.

Setup MySQL and Python drivers with the following command (run as root or with sudo)::

    apt-get install mysql-server python-mysqldb

Go through the wizard and set MySQL password.
Configure Ghiro to use MySQL as explained in configuration paragraph.

Apache as a front-end
---------------------

Now we are going to configure Apache as a front end for Ghiro's django
application.

Setup Apache and mod_wsgi with the following command (run as root or with sudo)::

    apt-get install apache2 libapache2-mod-wsgi

An example of virtual host configuration is the following (Ghiro is extracted in
/var/www/ghiro/ in this example)::

    <VirtualHost *:80>
        ServerAdmin webmaster@localhost
        WSGIProcessGroup ghiro
        WSGIDaemonProcess ghiro processes=5 threads=10 user=nobody group=nogroup python-path=/var/www/ghiro/ home=/var/www/ghiro/ display-name=local
        WSGIScriptAlias / /var/www/ghiro/ghiro/wsgi.py
        Alias /static/ /var/www/ghiro/static/
        <Location "/static/">
            Options -Indexes
        </Location>

        ErrorLog ${APACHE_LOG_DIR}/error.log

        # Possible values include: debug, info, notice, warn, error, crit,
        # alert, emerg.
        LogLevel warn

        CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>

Restart apache. Now the web application is listening on port 80/tcp, just put
the IP address in your browser.

Run the processor with upstart
------------------------------

You can automatically run the processor with upstart.

Create the file ghiro.conf in /etc/init/ with the following content::

    description     "Ghiro"

    start on started mysql
    stop on shutdown
    script
            chdir /var/www/ghiro/
            exec /usr/bin/python manage.py process
    end script

To stop the processor use the following command (run as root or with sudo)::

    service ghiro stop

To start the processor use the following command (run as root or with sudo)::

    service ghiro start
