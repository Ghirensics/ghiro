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
