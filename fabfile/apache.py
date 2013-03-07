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
#   limitations under the License.

from fabric.api import *
from cuisine import *

import utils

@task
def stop():
    with settings(warn_only=True):
        sudo("nohup service apache2 stop")
@task
def start():
    stop()
    sudo("nohup service apache2 start")

@task
def configure_ubuntu_packages():
    """Configure apache packages"""
    package_ensure('apache2')

@task
def uninstall_ubuntu_packages():
    """Uninstall apache packages"""
    package_clean('apache2')

@task
def configure(cluster=False,keystone_host="127.0.0.1",
              ec2_internal_url="http://127.0.0.1:8773/services/Cloud",
              compute_internal_url="http://127.0.0.1:8774/v1.1",
              keystone_internal_url="http://127.0.0.1:5000/v2.0",
              glance_internal_url="http://127.0.0.1:9292/v1",
              cinder_internal_url="http://127.0.0.1:8776/v1",
              quantum_internal_url="http://127.0.0.1:9696",
              portal_internal_url="http://127.0.0.1:8080/portal",
              activity_internal_url="http://127.0.0.1:8080/activity",
              chargeback_internal_url="http://127.0.0.1:8080/chargeback"):
    """Generate apache configuration. Execute on both servers"""
    configure_ubuntu_packages()
    if cluster:
        stop()
        sudo('echo "manual" >> /etc/init/apache2.override')
    sudo('mkdir -p /var/log/nova')
    sudo('a2enmod proxy_http')
    sudo('a2enmod ssl')
    sudo('a2enmod rewrite')
    sudo('a2ensite default-ssl')
    configure_apache(ec2_internal_url,compute_internal_url,keystone_internal_url,glance_internal_url,cinder_internal_url,quantum_internal_url,
                     portal_internal_url,activity_internal_url,chargeback_internal_url)
    configure_apache_ssl(ec2_internal_url,compute_internal_url,keystone_internal_url,glance_internal_url,cinder_internal_url,quantum_internal_url,
                         portal_internal_url,activity_internal_url,chargeback_internal_url)
    cert = text_strip_margin('''
        |-----BEGIN CERTIFICATE-----
        |MIICijCCAfOgAwIBAgIJAKiCfzU5EVkeMA0GCSqGSIb3DQEBBQUAMF4xCzAJBgNV
        |BAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEwHwYDVQQKDBhJbnRlcm5ldCBX
        |aWRnaXRzIFB0eSBMdGQxFzAVBgNVBAMMDiouc3RhY2tvcHMub3JnMB4XDTEyMDQy
        |NzA5MDQxNloXDTE1MDEyMTA5MDQxNlowXjELMAkGA1UEBhMCQVUxEzARBgNVBAgM
        |ClNvbWUtU3RhdGUxITAfBgNVBAoMGEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDEX
        |MBUGA1UEAwwOKi5zdGFja29wcy5vcmcwgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJ
        |AoGBANCh6DEOPNqjKVAkU0VSxSb8JgVWLnno5qgw/nXXNlIYF6kFL/I5ljZQHq0k
        |4rXl7bSwYVf9veEVZRPkMQJMeKnMZDrfAM/Azd8N1ukjBPID2oADd1nUrY1EQxpK
        |Nf20lgjs/H+MngLXVBfAVFT9n/KWYor0ClGxN/VaHMRz4VYpAgMBAAGjUDBOMB0G
        |A1UdDgQWBBTrLlSZSN4XPABtYMi+hSH42Mzz1DAfBgNVHSMEGDAWgBTrLlSZSN4X
        |PABtYMi+hSH42Mzz1DAMBgNVHRMEBTADAQH/MA0GCSqGSIb3DQEBBQUAA4GBAIod
        |Kyb8/xWqR/GXkk/l7LjrgrSs5tN9ah4k0Vai7oeKbbbNJ34eR6FwVUE13uxdHnsX
        |CdTM4LaLqFx2BUWhGfnaWsGHLj6bsb1bakpZF6g6DnFqrSloPUhrd1IMxZElTbjj
        |A+U3mBDyyhTeN+DsjvlESalFdbmuH63gwwmgKhMJ
        |-----END CERTIFICATE-----
        |''')
    key = text_strip_margin('''
        |-----BEGIN RSA PRIVATE KEY-----
        |MIICXQIBAAKBgQDQoegxDjzaoylQJFNFUsUm/CYFVi556OaoMP511zZSGBepBS/y
        |OZY2UB6tJOK15e20sGFX/b3hFWUT5DECTHipzGQ63wDPwM3fDdbpIwTyA9qAA3dZ
        |1K2NREMaSjX9tJYI7Px/jJ4C11QXwFRU/Z/ylmKK9ApRsTf1WhzEc+FWKQIDAQAB
        |AoGAUsQYR/W9AIN/7TIr8rFuUxPuxWk2ENjrQEgHeppBC3pRUJUlOzPLOoq4ULn0
        |UnL/xRG/3FdmT3fcXHLHWoEZ0JKxM3bnpBbD9U3tA79XHoZa84QSyGfyiQhRwQUD
        |wriuNMslA8sfA/9b+Ii/SLUJtTliTkPF+zmv4PnPTWmB7z0CQQD60g7R6GAILbaE
        |kqK02NiBsEOgpN8yGAPY1qNWQCZREul8AtAkRU8UGNrfS64Hjr7/BMA/RSnqHC1k
        |bIxEp9ILAkEA1PDTQ5DAUib8eV8KjNNpytt0fcdvtUX/J/KPrg1WeTv/JCeSFVKJ
        |f2OcEXh+llXKNnilkvbt+1zwXPS/yG7tGwJAXSFN22ba8W53zLXdsCSsD0txcN6G
        |+USteQAJWecr0wKgqykoO694c0/fRPYGwkugY3RSJav6qjCYMieT1ZIyjQJBAJpQ
        |5GmEjzt58WHr1HN2CqbuHx+/1l6iGWVTzXgvRkmZhy8mViGJrQdaopGupt4/0clj
        |6Wn19UVCdxaGcC3K5Z0CQQDt5qS1LbCsWNo3Mnz3q/iBF3b803YeD18darV03Ib7
        |8CVOK2mxVUn75jScoflQ9m7+yORF2+EdQNugLAas1d9O
        |-----END RSA PRIVATE KEY-----
        |''')
    configure_ssl(cert,key)
    start()

@task
def configure_apache(ec2_internal_url="http://127.0.0.1:8773/services/Cloud",
                     compute_internal_url="http://127.0.0.1:8774/v1.1",
                     keystone_internal_url="http://127.0.0.1:5000/v2.0",
                     glance_internal_url="http://127.0.0.1:9292/v1",
                     cinder_internal_url="http://127.0.0.1:8776/v1",
                     quantum_internal_url="http://127.0.0.1:9696",
                     portal_internal_url="http://127.0.0.1:8080/portal",
                     activity_internal_url="http://127.0.0.1:8080/activity",
                     chargeback_internal_url="http://127.0.0.1:8080/chargeback",
                     apache_conf=None):
    if apache_conf is None:
        apache_conf = text_strip_margin('''
        |
        |<VirtualHost *:80>
        |   ServerAdmin webmaster@localhost
        |
        |   ProxyPreserveHost On
        |   ProxyRequests Off
        |
        |   ProxyPass /services %s
        |   ProxyPassReverse /services %s
        |
        |   ProxyPass /compute/v1.1 %s
        |   ProxyPassReverse /compute/v1.1 %s
        |
        |   ProxyPass /keystone/v2.0 %s
        |   ProxyPassReverse /keystone/v2.0 %s
        |
        |   ProxyPass /glance/v1 %s
        |   ProxyPassReverse /glance/v1 %s
        |
        |   ProxyPass /volume/v1 %s
        |   ProxyPassReverse /volume/v1 %s
        |
        |   ProxyPass /network %s
        |   ProxyPassReverse /network %s
        |
        |   ProxyPass /portal %s
        |   ProxyPassReverse /portal %s
        |
        |   ProxyPass /activity %s
        |   ProxyPassReverse /activity %s
        |
        |   ProxyPass /chargeback %s
        |   ProxyPassReverse /chargeback %s
        |
        |   <Proxy *>
        |       Order allow,deny
        |       Allow from all
        |   </Proxy>
        |
        |   ErrorLog /var/log/nova/apache-error.log
        |   TransferLog /var/log/nova/apache-access.log
        |
        |</VirtualHost>
        |''' % (ec2_internal_url,ec2_internal_url,compute_internal_url,compute_internal_url,keystone_internal_url,
                keystone_internal_url,glance_internal_url,glance_internal_url,cinder_internal_url,cinder_internal_url,
                quantum_internal_url,quantum_internal_url,portal_internal_url,portal_internal_url,
                activity_internal_url,activity_internal_url,chargeback_internal_url,chargeback_internal_url))
    sudo('echo "%s" > /etc/apache2/sites-available/default' % apache_conf)

@task
def configure_apache_ssl(ec2_internal_url="http://127.0.0.1:8773/services/Cloud",
                         compute_internal_url="http://127.0.0.1:8774/v1.1",
                         keystone_internal_url="http://127.0.0.1:5000/v2.0",
                         glance_internal_url="http://127.0.0.1:9292/v1",
                         cinder_internal_url="http://127.0.0.1:8776/v1",
                         quantum_internal_url="http://127.0.0.1:9696",
                         portal_internal_url="http://127.0.0.1:8080/portal",
                         activity_internal_url="http://127.0.0.1:8080/activity",
                         chargeback_internal_url="http://127.0.0.1:8080/chargeback",
                         apache_conf=None):
    if apache_conf is None:
        apache_conf = text_strip_margin('''
        |
        |<IfModule mod_ssl.c>
        |<VirtualHost *:443>
        |   ServerAdmin webmaster@localhost
        |
        |   ProxyPreserveHost On
        |   ProxyRequests Off
        |
        |   ProxyPass /services %s
        |   ProxyPassReverse /services %s
        |
        |   ProxyPass /compute/v1.1 %s
        |   ProxyPassReverse /compute/v1.1 %s
        |
        |   ProxyPass /keystone/v2.0 %s
        |   ProxyPassReverse /keystone/v2.0 %s
        |
        |   ProxyPass /glance/v1 %s
        |   ProxyPassReverse /glance/v1 %s
        |
        |   ProxyPass /volume/v1 %s
        |   ProxyPassReverse /volume/v1 %s
        |
        |   ProxyPass /network %s
        |   ProxyPassReverse /network %s
        |
        |   ProxyPass /portal %s
        |   ProxyPassReverse /portal %s
        |
        |   ProxyPass /activity %s
        |   ProxyPassReverse /activity %s
        |
        |   ProxyPass /chargeback %s
        |   ProxyPassReverse /chargeback %s
        |
        |   <Proxy *>
        |       Order allow,deny
        |       Allow from all
        |   </Proxy>
        |
        |   ErrorLog /var/log/nova/apachessl-error.log
        |   TransferLog /var/log/nova/apachessl-access.log
        |
        |   SSLEngine on
        |   SSLCertificateFile /etc/ssl/certs/sslcert.crt
        |   SSLCertificateKeyFile /etc/ssl/private/sslcert.key
        |
        |   <FilesMatch "\.(cgi|shtml|phtml|php)$">
        |       SSLOptions +StdEnvVars
        |   </FilesMatch>
        |   <Directory /usr/lib/cgi-bin>
        |       SSLOptions +StdEnvVars
        |   </Directory>
        |
        |   BrowserMatch "MSIE [2-6]" nokeepalive ssl-unclean-shutdown downgrade-1.0 force-response-1.0
        |   # MSIE 7 and newer should be able to use keepalive
        |   BrowserMatch "MSIE [17-9]" ssl-unclean-shutdown
        |
        |</VirtualHost>
        |</IfModule>
        |''' % (ec2_internal_url,ec2_internal_url,compute_internal_url,compute_internal_url,keystone_internal_url,
                keystone_internal_url,glance_internal_url,glance_internal_url,cinder_internal_url,cinder_internal_url,
                quantum_internal_url,quantum_internal_url,portal_internal_url,portal_internal_url,
                activity_internal_url,activity_internal_url,chargeback_internal_url,chargeback_internal_url))
    sudo('''echo '%s' > /etc/apache2/sites-available/default-ssl''' % apache_conf)

@task
def configure_ssl(cert,key):
    """Upload .crt and .key files to server"""
    sudo('echo "%s" > /etc/ssl/certs/sslcert.crt' % cert)
    sudo('echo "%s" > /etc/ssl/private/sslcert.key' % key)
