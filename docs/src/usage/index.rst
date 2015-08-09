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
