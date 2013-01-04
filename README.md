FABULOSO - Scripts to deploy Openstack-based architectures
==========================================================

1.- Bootstrap the Operating System

The scripts needs some basic configuration to work:
- An openssh-server installed
- The stackops user without password and member of the sudo group
- A public key. With the scripts comes a non secure private/public key combo for default installation. Please change it
  asap.

The bootstrap script for any OS with a Bourne shell is very simple. You can use it like this:

wget -O - https://raw.github.com/StackOps/fabuloso/master/bootstrap/init.sh | sudo sh

2.- Configuring the network

Depending on the component type, you will have to configure the network with different number of interfaces and
configurations.