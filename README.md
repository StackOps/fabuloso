Command line shell and API remote executor
=====================================================

## What is FABULOSO?

Fabuloso is a script executor that handles plugable components
inside a catalog and configurable remote environments using
providers. In StackOps we use FABULOSO mainly to manage OpenStack
deployments.

### What is a component

A component is just a directory that holds a python module and
 a configuration file. Configuration file defines which functions of
 the module are exposed to fabuloso and the name of the component. For
 instance, the embedded 'mysql' configuration file is:

```ini
[component]

name = mysql
file = mysql.py
provider = fabric
methods = 
    configure
    start
    stop
```

Then, the file mysql.py is the module that holds the methods 'configure',
'start' and 'stop'.

### What is a catalog

The catalog is the list of directories where fabuloso searches into
to look for components. These components are loaded dynamically in each
fabuloso execution.

### What is an environment

Environments are a set properties to define a remote connection. All the 
executions that fabuloso performs run in that remote connection. The configuration
file (in your $HOME/.config/fabuloso/config.py) defines a couple of remote
executions. If you don't specify anything (via shell or via API, fabuloso
will use the 'default' one). 

You can switch between environments as many times as you wish (TODO!)

### What is a provider

Provider is the actual executor of the scripts. Currently we only support
the 'fabric' provider

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

```
fabuloso > help

Documented commands (type help <topic>):
========================================
help  mysql  quit

fabuloso >
```

and execute them!

#### API

Fabuloso provides a simple API as well. A simple program would be:

```python

import fabuloso

env_dict = {
    "host": "localhost",
    "port": 2223,
    "username": "stackops",
    "ssh_key_file": "~/.ssh/nonsecureid_rsa"
}

env = fabuloso.RemoteEnvironment(env_dict)

fab = fabuloso.Fabuloso(env)
fab.execute("mysql", "start")
```

### What license do you use?

Apache 2.0 license, of course. (TO CHANGE)
