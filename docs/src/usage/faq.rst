FAQ
===

How to install GExiv2 on a virtualenv?
--------------------------------------

First of all setup GExiv2 on your system installing it the  usual way, for example with apt-get.
Now you have two ways to get it working on a virtualenv.
The first is create your virtualenv starting from system packages. The ```--system-site-packages```
option links the public packages installed on the system to the new virtual environment.
The second one is to symlink the GExiv2 library from your virtualenv with::

    $ cd virtualenv
    $ cd lib/python2.7/
    $ ln -s /usr/lib/python2.7/dist-packages/gi

How to submit a bug report
--------------------------

If you encounter an issue with Ghiro or if you want to suggest a new feature,
you are welcome to `submit a new issue`_.

If you are filling a bug report you should always follow this template:

#. What were you doing?
#. What did you expect to happen?
#. What happened instead?
#. Ghiro release of Ghiro Appliance release.
#. Browser and Version of Browser, Operating
   System running Browser.
#. If you are reporting a UI issue screenshot(s) showing the problem.

.. _`submit a new issue`: https://github.com/Ghirensics/ghiro/issues/new

Is Ghiro uploading my data somewhere?
-------------------------------------

Absolutely no. Ghiro is a tool designed for forensic's professionals, law enforcement, and
generally people working with critical data related to an investigation.
We put great attention in protecting users privacy and security.
Ghiro does not upload or disclose your data in any way. Your data are stored in your
database and never leave it.
Ghiro only contacts, once per day, the update server (located at update.getghiro.org) with a
simple HTTP request to check if a new release is available. If you don't like this, you
can disable the update check editing local_settings.py and setting::

    UPDATE_CHECK = False

If you set this to false no connection will be opened.