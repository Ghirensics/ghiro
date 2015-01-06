Usage
=====

Ghiro's web application is composed by several parts to organize information and
analysis data.

Dashboard
---------

This is the summary of all Ghiro activities, here you can figure what is going
on, which are the last cases and analysis, and take a look to analysis trend.

Cases
-----

Image analysis are grouped in cases. Different users and permissions can be
assigned to each case.
You can upload images via an upload in many ways:

 * You can add some images using your browser using the "Add image" method
 * You can add an image from an URL using the "Add URL" method
 * You can add images from a folder in Ghiro's server giving his path with the "Add folder" method
 * You can add images from a folder in Ghiro's server via command line

Images
------

Here you can see all image analysis in the system (all images you have permission to see).

Search
------

You can search for several image properties or for image location.
Search is available also inside a case, to have the search scope restricted to
the case.

Hashes
------

Sometimes hash lists are used to search and match a special kind of images you
already have an hash.
A text file with a list, one per line, of image's hashes can be loaded in Ghiro
with a label and a description. If Ghiro detects an image with an hash matching
your hash list, it will trigger a signature and warn you.

Administration
--------------

In Ghiro's administration panel you can:

 * Administer all Ghiro's users
 * See user's activity log
 * Check for required dependencies

Administration
==============

Some hints about Ghiro administration.

Run processor in debug mode
---------------------------

If you need to run the image processor daemon in debug mode to debug tracebacks
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

If you want to add the image located at /target/image.jpg to case with id
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
