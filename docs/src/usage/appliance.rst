Virtual Appliance
=================

The fastest way to start playing with Ghiro is to download the Ghiro Virtual
Appliance.
You can download it from the `official website`_.
In few minutes you will have a fully functional Ghiro setup, running in a
virtual machine, to start to analyze your images.
It is an OVA file, you have to import in your virtualization software (like
VirtualBox or VMWare) and configure the networking as explained in the
documentation.

Getting Started
---------------

Import the .OVA file in your virtualization software (VirtualBox or Vmware).
For example in VirtualBox go in File > Import Appliance and select the .OVA file.
Start the appliance.

The appliance credentials are:
Username: ghiro
Password: ghiromanager

For extra security, remember to change the password at your first access.

The first time you have to properly configure the network interface.
Select the virtual networking you like (for example
bridged or NAT); by default the appliance is configured in bridged mode.
By default, Ghiro appliance will get an IP address using DHCP and show it in
the boot screen.

If you need to manually configure your IP address: login in, and configure the
networking card with your desired IP, for example to
give the IP 192.168.0.10 use the following command:

sudo ifconfig eth0 192.168.0.10 up

When Ghiro appliance has an IP address, via DHCP or via manual configuration,
the web interface is reachable on default HTTP port 80/tcp, just put the
appliance address in your browser. For example:

http://192.168.0.10 (or other DHCP or manually configured address)

The web interface credentials are:
Username: ghiro
Password: ghiromanager

For extra security, remember to change the password at your first access.

Now you can start analyzing images! Go in the "Cases" panel, create your first
case, and add your images with the add button.
For usage help please refer to the documentation at:
http://www.getghiro.org/docs/latest/usage/index.html

If you need to access remotely to the appliance you can use SSH.
The appliance is shipped with a default disk of 50GB, if is not enough you can
create another virtual disk and add that to the root volume using LVM.

Appliance building
------------------

The appliance building script is open source and available under a project
dubbed `ghiro-appliance`_ on Github.

Ghiro appliance builder is a `packer.io`_ script to automagically create a Ghiro
appliance ready to be used, based on Ubuntu.

Using this script you should be able to create your onw Ghiro appliance updated
to Ghiro's developed branch. You can easily customize the appliance building
script to have your own customized appliance.

.. _`packer.io`: http://packer.io
.. _`ghiro-appliance`: https://github.com/ghirensics/ghiro-appliance