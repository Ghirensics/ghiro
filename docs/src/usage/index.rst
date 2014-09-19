Usage
=====

Ghiro's web application is composed by several parts to organize information and analysis data.

Dashboard
---------

This is the summary of all Ghiro activities, here you can figure what is going on, which are the last
cases and analysis, and take a look to analysis trend.

Cases
-----

Image analysis are grouped in cases. Different users and permissions can be assigned to each case.
You can upload images via an upload form ("Add image" function) or you can get the images from a
path on the Ghiro's server ("Add folder" function).
Here you can see all analysis related to images grouped by case.

Images
------

Here you can see all image analysis in the system (all images you have permission to see).

Search
------

You can search for several image properties or for image location.

Hashes
------

You can load hash lists to detect if an image met an hash.

Administration
--------------

Ghiro user administration: you can administer all Ghiro's users.

Administration
==============

Some hints about Ghiro administration.

Run processor in debug mode
---------------------------

If you need to run the image processor deamon in debug mode to debug tracebacks
run the following command (inside Ghiro's root)::

    python manage.py process --traceback

Create a new superuser
----------------------

If you need to create a new superuser from the command lince, for example
because you closed you out from the web interface, run the following command
(inside Ghiro's root)::

    python manage.py createsuperuser

Upload images via command line utility
--------------------------------------

You can analyze images from command line with the submit utility.
It can load and submit for analysis: an image, a folder containing images, a folder containing
images and other folders, and recurse inside them.

If you want to add the image located at /target/imageimage.jpg to case with id
2 and owner user name "foobar" run the following command (inside Ghiro's root)::

    python manage.py submit -u foobar -c 2 -t /target/image.jpg

If you want to add all images in folder /target/images to case with id
2 and owner user name "foobar" run the following command (inside Ghiro's root)::

    python manage.py submit -u foobar -c 2 -t /target/images

If you want to add all images in folder /target/images and all subfolders to case with id
2 and owner user name "foobar" run the following command (inside Ghiro's root)::

    python manage.py submit -u foobar -c 2 -t /target/images -r

If you need to load tons of images this utility is designed for you,
all images could be loaded in a single batch.

Check for updates
-----------------

Ghiro automatically checks for new updates every day, if you don't disable the
update check.
Anyway a command line command is available to manually check for updates::

    python manage.py update_check

Save all images
---------------

If you need to dump all images in Ghiro's database, in their original format, to
disk, you can save all to disk with::

    python manage.py images_save_all -p /path/to/disk/
