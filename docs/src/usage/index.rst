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

Auto Upload
-----------

Auto Upload is a feature to automatically upload images written in a default directory; you can
share the default directory over FTP, Samba (Windows shared folder) or other file sharing technologies
so you can simply launch a Ghiro analysis copying a file in a shared folder.

To configure Auto Upload you have to edit `local_settings.py` and configure:

 * `AUTO_UPLOAD_DIR` to the directory you want to use for Ghiro Auto Upload
 * (optional) `AUTO_UPLOAD_DEL_ORIGINAL` if you want to keep the original files (it is suggested to keep the default value, files will be deleted after being submitted to Ghiro)
 * (optional) `AUTO_UPLOAD_STARTUP_CLEANUP` if you don't want to clean `AUTO_UPLOAD_DIR` at startup (it is suggested to keep the default value, `AUTO_UPLOAD_DIR` will be cleaned up at startup)

After configuration, you have to start the directory monitoring with the following command::

    python manage.py auto_upload

Now directory monitoring is running, a tree of folder related to cases in your system will be created,
for example:

.. image:: ../_images/auto_upload_folders.png

As you can see there are many folder, one for each case stored, with the case id in the folder name.
You should only put the images you want to be analyzed inside a case folder, ghiro will automatically
process them, store inside the case with the same id of the folder name, and remove the original file
from disk.

This feature comes to help in many situations:

 * When you need to provide people an easy way to submit images to Ghiro, you could just setup a shared folder.
 * If you need to analyze a large amount of data, you could submit with a files copy command.

.. warning::
        Don't use the Auto Upload directory configured in `AUTO_UPLOAD_DIR` as a permanent storage!
        Depending on the configuration, it will be cleaned up each time you run `manage.py auto_upload`.
        Auto Upload directory is designed as temporary storage to submit images only.

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
