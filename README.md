FABULOSO - Scripts to deploy Openstack-based architectures
==========================================================

h1. Bootstrap the Operating System

h2. Installation script
The scripts needs some basic configuration to work:
- An openssh-server installed
- The stackops user without password and member of the sudo group
- A public key. With the scripts comes a non secure private/public key combo for default installation. Please change it
  asap.

The bootstrap script for any OS with a Bourne shell is very simple. You can use it like this:

```shell
wget -O - https://raw.github.com/StackOps/fabuloso/master/bootstrap/init.sh | sudo sh
```

h2.  Configuring the network

Depending on the component type, you will have to configure the network with different number of interfaces and
configurations.


h1. How to mimic the StackOps discovery agent

h2. Why you need it
Sometimes you will need to perform a manual installation of a node without the discovery process. You need to perform
the following steps:

If you want to perform a manual discovery of your existing nodes you can follow these steps:

h2. Install the StackOps Community Distro in the node

And configure the network manually during the installation.

h2. Change the network configuration

Perform the following steps:

# Log into the server as root, and modify the /etc/network/interfaces file. The eth0 interface must be in dhcp mode.
# Delete the entries in /etc/hosts referencing the old network configuration
# Reboot the server

h2. Execute the fake discovery script

The fake discovery script works for StackOps Distro and Ubuntu 12.04 Server OS. Login as root and execute:

````shell
wget -O - https://raw.github.com/StackOps/fabuloso/master/bootstrap/fake-discovery.sh | sudo sh
```

After a few seconds you will see the server in the Head-Manager Pool. The server is 'hot spare' spare server.

h3. Configure IPMI parameters of the servers

It's a good practice to configure the IPMI IP for management of the new node:

```shell
head-manage pool modify MAC lom_ip IPMI_IP
```

Remember that the username and password are stored in the parameters of the zone.

h3. Active the hot spare server in the zone.

ACtive the hot spare server following the same process used for standard discovered nodes in the pool. The 
configuration process will start.
