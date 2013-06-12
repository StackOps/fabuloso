FABric scripts with steroids
============================

## What is FABuloso?

Fabuloso is a fabric script executor that handles plugable components
inside a catalog and configurable remote environments. 
In StackOps we use FABuloso mainly to manage OpenStack
deployments.

### What is a Component

A component is just a directory that holds a python module and
 a configuration file.
 
 Configuration file defines which services of
 the module are exposed to be executed. For
 instance, the embedded 'mysql' configuration file is:

```yaml
name: mysql
file: mysql.py
description: MySQL database component

Services:
    - name: setup
      description: Installs a mysql service and runs it
      methods:
          - configure
          - start
    - name: teardown
      description: Stops the mysql service
      methods:
          - stop
```

The *component* name is 'mysql' and exposes the services 'setup' and 'teardown'.
Each *service* wraps one or more module *methods*. These methods are actually
defined in the actual python module.

These components are loaded dynamically when a Fabuloso instance is created.

### What is a catalog

The catalog is the list of directories where fabuloso searches into
to look for components. You can define as many as directories as you wish in 
the [config](TODO) file.

### What is an environment

Environments are a set properties to define a remote connection. All the 
executions that fabuloso performs run in that remote connection. The [configuration
file](TODO) define the remote executions in the [shell way](TODO). You
can also create your own environment programatically and use it to instance
a new Fabuloso instance in the [API way].

## Getting Started

### Installation

Download the source code an perform:

```python
python setup.py install
```

Fabuloso is in deep development, so we recommend to use it into a virtual environment.


### Configuration

After install it, check out your ($HOME/.config/fabuloso/config.py) and set the
environments you wish giving to each of them a different name. Modify as well the
list of catalog directories.


### Run it

#### Shell

To run fabuloso in shell just type:

```bash
$ fabuloso
``` 

in the command line. (User $ fabuloso -e 'environment_name' if you don't wish to start with the default environment)

Check out the component using help:

```bash
fabuloso > help
Available components are:

* mysql
* os

fabuloso >
```

Then you can chek the services available per component:

```bash
fabuloso > help os
Available services for this component are:

* info: Return as machine info as it can collect
        - No params
* setup_os: Sets all the actions to prepare a StackOps deployment
        - No params
fabuloso > 
```


and execute them!

#### API

Fabuloso provides a simple API to execute the services. A simple program would be:

```python

catalog = ['/path/to/catalog']

env_dict = {
    "host": "localhost",
    "port": 2223,
    "username": "stackops",
    "ssh_key_file": "~/.ssh/nonsecureid_rsa"
}

mysql_properties = {
    'root_pass' = 'root'
}

fab = fabuloso.Fabuloso(catalog)
mysql = fabuloso.get_component('mysql', mysql_properties, env_dict)
mysql.install()

```

This code:
* first define the directory where fabuloso will search into the
list of components
* Then defines the environment where the component will be executed
* Then defines the properties of the component
* Instantiates fabuloso with the catalog directory
* Gets an instance of the component with the properties and the environment
* It runs the 'install' service defined by the 'component.yml' definition file
  of the component


See the [wiki](TODO) to more information

### What license do you use?

Apache 2.0 license.
