#   Copyright 2012-2013 STACKOPS TECHNOLOGIES S.L.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.from fabric.api import *

from fabric.api import *
from cuisine import *

@task
def stop():
    with settings(warn_only=True):
        sudo("/etc/init.d/nfsen stop")

@task
def start():
    stop()
    sudo("/etc/init.d/nfsen start")

@task
def configure_ubuntu_packages():
    """Configure nfsen packages"""
    package_ensure('apache2 nfdump rrdtool mrtg librrds-perl librrdp-perl librrd-dev libmailtools-perl php5 bison flex')

@task
def uninstall_ubuntu_packages():
    """Uninstall nfsen packages"""
    package_clean('nfdump rrdtool mrtg librrds-perl librrdp-perl librrd-dev libmailtools-perl php5 bison flex')

@task
def install():
    """Generate nfsen install."""
    configure_ubuntu_packages()
    with settings(warn_only=True):
        sudo('sudo useradd -d /var/netflow -G www-data -m -s /bin/false netflow')
    with cd('/usr/local/src'):
        sudo('wget https://stackops.s3.amazonaws.com/nfsen-1.3.6p1.tar.gz -O ./nfsen-1.3.6p1.tar.gz')
        sudo('tar xvzf nfsen-1.3.6p1.tar.gz')

@task
def configuration():
    """Generate nfsen configuration."""
    with cd('/usr/local/src/nfsen-1.3.6p1'):
        nfsenconf = text_strip_margin('''
            |$BASEDIR = "/var/lib/nfsen";
            |$BINDIR="${BASEDIR}/bin";
            |$LIBEXECDIR="${BASEDIR}/libexec";
            |$CONFDIR="${BASEDIR}/etc";
            |$HTMLDIR    = "/var/www/nfsen/";
            |$DOCDIR="${HTMLDIR}/doc";
            |$VARDIR="${BASEDIR}/var";
            |$PROFILESTATDIR="${BASEDIR}/profiles-stat";
            |$PROFILEDATADIR="${BASEDIR}/profiles-data";
            |$BACKEND_PLUGINDIR="${BASEDIR}/plugins";
            |$FRONTEND_PLUGINDIR="${HTMLDIR}/plugins";
            |$PREFIX  = "/usr/bin";
            |$USER    = "netflow";
            |$WWWUSER  = "www-data";
            |$WWWGROUP = "www-data";
            |$BUFFLEN = 2000;
            |$SUBDIRLAYOUT = 1;
            |$ZIPcollected    = 1;
            |$ZIPprofiles     = 1;
            |$PROFILERS = 2;
            |$DISKLIMIT = 98;
            |$PROFILERS = 6;
            |%sources = (
            |    "upstream1"    => { "port" => "555", "col" => "#0000ff", "type" => "netflow" },
            |);
            |$low_water = 90;
            |$syslog_facility = "local3";
            |@plugins = (
            |# profile    # module
            |# [ "*",     "demoplugin" ],
            |);
            |
            |%PluginConf = (
            |    # For plugin demoplugin
            |    demoplugin => {
            |    # scalar
            |    param2 => 42,
            |              # hash
            |              param1 => { "key" => "value" },
            |},
            |# for plugin otherplugin
            |otherplugin => [
            |                   # array
            |                   "mary had a little lamb"
            |               ],
            |);
            |$MAIL_FROM   = "your@from.example.net";
            |$SMTP_SERVER = "localhost";
            |$MAIL_BODY       = q{
            |    Alert "@alert@" triggered at timeslot @timeslot@
            |};
            |
            |1;''')
        sudo('''echo '%s' > etc/nfsen.conf''' % nfsenconf)
        sudo('perl install.pl etc/nfsen.conf')
        with settings(warn_only=True):
            sudo('ln -s /var/lib/nfsen/bin/nfsen /etc/init.d/nfsen')
            sudo('update-rc.d nfsen defaults 20')

