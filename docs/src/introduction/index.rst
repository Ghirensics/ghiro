Why Ghiro?
==========

Sometime forensic investigators need to process digital images as evidence.
There are some tools around, most of them are little scripts, otherwise it is
difficult to deal with forensic analysis with many images involved.
Digital images contain tons of information, it is a thediuos work to manually
extract all of them, Ghiro extracts these information from provided images and
display them in a nicely formatted report.
Dealing  with tons of images has never been so easy, Ghiro is designed to scale 
to support gigs of images.
All tasks are totally automated, you have just to upload your images and let
Ghiro do the work.
Understandable reports and great search capabilities allows you to find a needle
in a haystack.
Ghiro is a multi user environment, different permissions can be assigned to each
user.
Cases allow you to group image analyses by topic, you can choose which user
allow to see your case with a permission schema. Every team in your forensic lab
could work in their own cases with privileges separation.

Use Case
========

Ghiro can be used in many scenarios, forensic investigators could use it on
daily basis in their analysis lab but also people interested to undercover
secrets hidden in images could benefit.
Some use case examples are the following:

 * If you need to extract all data and metadata hidden in an image in a fully automated way
 * If you need to analyze a lot of images and you have not much time to read the report for all them
 * If you need to search a bunch of images for some metadata
 * If you need to geolocate a bunch of images and see them in a map
 * If you have an hash list of "special" images and you want to search for them

Anyway Ghiro is designed to be used in many other scenarios, the imagination is
the only limit.

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

 * The web interface: to interact with all features, this is the component used by users to work with Ghiro
 * The processor daemon: it fetches waiting tasks from the queue, process and analyze images
 * The SQL database: it stores relational data, you can choose between MySQL, PostgreSQL and SQLite3
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

Verifying Signatures
====================

Every release published by the Ghiro Developers is digitally signed by the
`Ghiro Master Signing key`_ or by one of the developers (each such key is signed
by the `Ghiro Master Signing key`_).

The first step is to import the Ghiro Master Signing public key, you can download
it from a keyserver with this command::

    $ gpg --keyserver pool.sks-keyservers.net --recv-keys 0xafda03a581c21ee9

You can add it directly from Ghiro website too::

    $ gpg --fetch-keys http://getghiro.org/keys/ghiro_master_signing_key.asc

The fingerprint of `Ghiro Master Signing key`_ is published here (for additional security)::

    9DD9 3A61 39A4 A72D 2467  378D AFDA 03A5 81C2 1EE9

Now you can download the signature for Ghiro package or appliance from Ghiro website,
you can verify it with the following::

    $ gpg --verify ghiro-0.2.zip.sig
    gpg: Signature made Sun Mar 15 17:55:51 2015 CET using RSA key ID 81C21EE9
    gpg: Good signature from "Ghiro Master Signing key (Ghiro Master Signing key)" [ultimate]

If you get an output like this one, the package you got is good and you can trust it,
if you get a different output you are facing a security risk, you should contact Ghiro's
developers and never use the downloaded package.

It is also a good, although optional, practice to set its trust level to “ultimate”,
so that it can be used to automatically verify all the keys signed by the Ghiro developers::

    $ gpg –edit-key 0x81C21EE9

Now trust the key, and set trust to ultimate level with::

    gpg> trust pub 4096R/81C21EE9

As example the full output follows::

    $ gpg --keyserver pool.sks-keyservers.net --recv-keys 0xafda03a581c21ee9
    gpg: requesting key 81C21EE9 from hkp server pool.sks-keyservers.net
    gpg: /home/jekil/.gnupg/trustdb.gpg: trustdb created
    gpg: key 81C21EE9: public key "Ghiro Master Signing key (Ghiro Master Signing key)" imported
    gpg: no ultimately trusted keys found
    gpg: Total number processed: 1
    gpg:               imported: 1  (RSA: 1)

    $ gpg --edit-key 0x81C21EE9
    gpg (GnuPG) 1.4.16; Copyright (C) 2013 Free Software Foundation, Inc.
    This is free software: you are free to change and redistribute it.
    There is NO WARRANTY, to the extent permitted by law.


    pub  4096R/81C21EE9  created: 2015-03-15  expires: 2021-03-15  usage: SC
                         trust: unknown       validity: unknown
    sub  4096R/E51F5BBD  created: 2015-03-15  expires: 2021-03-15  usage: E
    [ unknown] (1). Ghiro Master Signing key (Ghiro Master Signing key)

    gpg> trust pub 4096R/81C21EE9
    pub  4096R/81C21EE9  created: 2015-03-15  expires: 2021-03-15  usage: SC
                         trust: unknown       validity: unknown
    sub  4096R/E51F5BBD  created: 2015-03-15  expires: 2021-03-15  usage: E
    [ unknown] (1). Ghiro Master Signing key (Ghiro Master Signing key)

    Please decide how far you trust this user to correctly verify other users' keys
    (by looking at passports, checking fingerprints from different sources, etc.)

      1 = I don't know or won't say
      2 = I do NOT trust
      3 = I trust marginally
      4 = I trust fully
      5 = I trust ultimately
      m = back to the main menu

    Your decision? 5
    Do you really want to set this key to ultimate trust? (y/N) y

    pub  4096R/81C21EE9  created: 2015-03-15  expires: 2021-03-15  usage: SC
                         trust: ultimate      validity: unknown
    sub  4096R/E51F5BBD  created: 2015-03-15  expires: 2021-03-15  usage: E
    [ unknown] (1). Ghiro Master Signing key (Ghiro Master Signing key)
    Please note that the shown key validity is not necessarily correct
    unless you restart the program.

    gpg> quit

.. _`Ghiro Master Signing key`: http://getghiro.org/keys/ghiro_master_signing_key.asc