FABULOSO - Scripts to deploy Openstack-based architectures
==========================================================

# What is FABULOSO?

FABuloso is a set of lightweight Fabric scripts built to deploy Openstack like always should be: easy.

## What is Fabric?

## What is Vagrant?

## How do I install Vagrant?

## How do I install Fabric in my compute?

## Another deployment tool for Openstack???? AGGGGHHHHH!!!!!

Relax. This is how StackOps deploys and manages Openstack clouds. There are really cool tools our there, but we
think we have to focus in doing things simpler and easier.

We think the Openstack community suffers of the 'Golden Hammer' syndrome about all these nice deployment toos.
FABuloso only does what it does, and it does it very well.

## What license do you use?

Apache 2.0 license, of course.

## This looks cool! Can I colaborate?

Sure, just push it.

## What version of Openstack is supported?

Right now folsom stable. Just check the branches to see different versions. Obvioulsy this will change.


# Deployment example of a single node on Vagrant


## Install fabric

If you are using Ubuntu 12.04 LTS or newer.
```shell
       sudo apt-get install fabric
```

## Vagrant

Create the  directory where you want to create your vagrant environment. for example:

```shell
       mkdir fabuloso
```

## Download our test box

Go to the directory that you have crated and download the stackops box

```shell
       cd fabuloso/
       vagrant box add stackops-distro-base-v2 https://dl.dropbox.com/u/527582/stackops-distro-base-v2.box
```

## Download the FABuloso repository in the same directory

```shell
       git clone git@github.com:StackOps/fabuloso.git
```

## Run the box stackops-distro-base-v2

```shell
       vagrant up
```

## Execute singlenode.sh file to configurate your box.

This can take a while.
```shell
       ./singlenode.sh
```

# Running FABuloso in other operating Systems. Bootstrapping

## Installation script
The scripts needs some basic configuration to work:
- An openssh-server installed
- The stackops user without password and member of the sudo group
- A public key. With the scripts comes a non secure private/public key combo for default installation. Please change it
  asap.

The bootstrap script for any OS with a Bourne shell is very simple. You can use it like this:

```shell
wget -O - https://raw.github.com/StackOps/fabuloso/master/bootstrap/init.sh | sudo sh
```

##  Configuring the network

Depending on the component type, you will have to configure the network with different number of interfaces and
configurations.


# How to mimic the StackOps discovery agent

## Why you need it
Sometimes you will need to perform a manual installation of a node without the discovery process. You need to perform
the following steps:

If you want to perform a manual discovery of your existing nodes you can follow these steps:

## Install the StackOps Community Distro in the node

And configure the network manually during the installation.

## Change the network configuration

Perform the following steps:

1. Log into the server as root, and modify the /etc/network/interfaces file. The eth0 interface must be in dhcp mode.
2. Delete the entries in /etc/hosts referencing the old network configuration
3. Reboot the server

# Execute the fake discovery script

The fake discovery script works for StackOps Distro and Ubuntu 12.04 Server OS. Login as root and execute:

````shell
wget -O - https://raw.github.com/StackOps/fabuloso/master/bootstrap/fake-discovery.sh | sudo sh
```

After a few seconds you will see the server in the Head-Manager Pool. The server is 'hot spare' spare server.

## Configure IPMI parameters of the servers

It's a good practice to configure the IPMI IP for management of the new node:

```shell
head-manage pool modify MAC lom_ip IPMI_IP
```

Remember that the username and password are stored in the parameters of the zone.

## Active the hot spare server in the zone.

ACtive the hot spare server following the same process used for standard discovered nodes in the pool. The 
configuration process will start.
