Why Ghiro?
==========

Sometime forensic investigators need to process digital images as evidence.
There are some tools around, otherwise it is difficult to deal with forensic analysis with many
images involved.
Images contain tons of information, Ghiro extracts these information from provided images and
display them in a nicely formatted report.
Dealing  with tons of images has never been so easy, Ghiro is designed to scale to support gigs of images.
All tasks are totally automated, you have just to upload you images and let Ghiro does the work.
Understandable reports, and great search capabilities allows you to find a needle in a haystack.
Ghiro is a multi user environment, different permissions can be assigned to each user.
Cases allow you to group image analysis by topic, you can choose which user allow to see your case
with a permission schema.

Use Case
========

Ghiro can be used in many scenarios, forensic investigators could use it on daily basis in
their analysis lab but also people interested to undercover secrets hidden in images could
benefit.
Some use case examples are the following:

 * If you need to extract all data and metadata hidden in an image in a fully automated way
 * If you need to analyze a lot of images and you have not much time to read the report for all them
 * If you need to search a bunch of images for some metadata
 * If you need to geolocate a bunch of images and see them in a map
 * If you have an hash list of "special" images and you want to search for them

Anyway Ghiro is designed to be used in many other scenarios, the imagination is the only limit.


Supported image types
=====================

The following file type are supported:

 * Windows bitmap .bmp
 * Raw Canon .cr2
 * Raw Canon .crw
 * Encapsulated PostScript .eps
 * Graphics Interchange Format .gif
 * JPEG File Interchange Format .jpg or .jpeg
 * Raw Minolta .mrw
 * Raw Olympus .orf
 * Portable Network Graphics .png
 * Raw Photoshop .psd
 * Raw Fujifilm .raf
 * Raw Panasonic .rw2
 * Raw TARGA .tga
 * Tagged Image File Format .tiff

Architecture
============

Ghiro is composed by the following components:

 * The web interface: to interact with all features
 * The processor deamon: it fetches waiting tasks from the queue, process and analyze images
 * The relation database: it stores relational data, you can choose between MySQL, PostgreSQL and SQLite3
 * The MongoDB database: it stores analysis data

Following the architecture in a simple schema:

.. image:: ../_images/architecture.png

Download Ghiro
==============

Ghiro can be downloaded from the `official website`_, where the stable and
packaged releases are distributed. Stable package is available in both
.zip and .tar.gz format.
The package above is strongly suggested for all users.
Some people need to keep updated with Ghiro's changes, they can download
(git clone) from our `official GitHub page`_.
There are two different releases available.

Development Branch
------------------

The development branch is where the next Ghiro's release is developed.
You can download Ghiro from here if you need to keep it always at the
cutting edge or if you want to hack on Ghiro.
You can download it with the following command::

    git clone https://github.com/ghirensics/ghiro.git

.. warning::
        While being more updated, the development branch should be
        considered an *under development*.
        Therefore its stability is not guaranteed.

.. _`official website`: http://www.getghiro.org
.. _`official GitHub page`: https://github.com/ghirensics/ghiro

Virtual Appliance
=================

The faster way to start playing with Ghiro is to download the Ghiro Virtual Appliance.
You can download it from the `official website`_.
In few minutes you will have a fully functional Ghiro setup to start to analyze your images.
It is an OVA file, you have to import in your virtualization software (like VirtualBox or
VMWare) and configure the networking as explained in the documentation.
Just unzip the archive and read the README.txt file!