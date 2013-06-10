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
from fabric.api import settings, sudo
from cuisine import (package_ensure, package_clean, text_strip_margin,
                     file_write)


def configure(keystone_host, ec2_internal_url,
              compute_internal_url, keystone_internal_url,
              glance_internal_url, cinder_internal_url,
              quantum_internal_url, portal_internal_url=None,
              activity_internal_url=None, chargeback_internal_url=None,
              common_name='127.0.0.1'):
    """Generate apache configuration. Execute on both servers"""

    sudo('mkdir -p /var/log/nova')
    sudo('a2enmod proxy_http')
    sudo('a2enmod ssl')
    sudo('a2enmod rewrite')
    sudo('a2ensite default-ssl')
    _configure_default(ec2_internal_url, compute_internal_url,
                       keystone_internal_url, glance_internal_url,
                       cinder_internal_url, quantum_internal_url,
                       portal_internal_url, activity_internal_url,
                       chargeback_internal_url)
    _create_certs(common_name)
    _configure_apache_ssl(ec2_internal_url, compute_internal_url,
                          keystone_internal_url, glance_internal_url,
                          cinder_internal_url, quantum_internal_url,
                          portal_internal_url, activity_internal_url,
                          chargeback_internal_url)


def stop():
    with settings(warn_only=True):
        sudo("nohup service apache2 stop")


def start():
    stop()
    sudo("nohup service apache2 start")


def install():
    """Configure apache packages"""
    package_ensure('apache2')


def uninstall():
    """Uninstall apache packages"""
    package_clean('iptables-persistent')
    package_clean('apache2')


def _configure_default(ec2_internal_url, compute_internal_url,
                       keystone_internal_url, glance_internal_url,
                       cinder_internal_url, quantum_internal_url,
                       portal_internal_url, activity_internal_url,
                       cb_internal_url, apache_conf=None):
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
        |''' % (ec2_internal_url, ec2_internal_url, compute_internal_url,
                compute_internal_url, keystone_internal_url,
                keystone_internal_url, glance_internal_url,
                glance_internal_url, cinder_internal_url, cinder_internal_url,
                quantum_internal_url, quantum_internal_url))

        if portal_internal_url is not None:
            apache_conf += text_strip_margin('''
            |
            |   ProxyPass /portal %s
            |   ProxyPassReverse /portal %s
            |
            ''') % (portal_internal_url, portal_internal_url)

        if activity_internal_url is not None:
            apache_conf += text_strip_margin('''
            |
            |   ProxyPass /activity %s
            |   ProxyPassReverse /activity %s
            |
            ''') % (activity_internal_url, activity_internal_url)

        if cb_internal_url is not None:
            apache_conf += text_strip_margin('''
            |
            |   ProxyPass /chargeback %s
            |   ProxyPassReverse /chargeback %s
            |
            ''') % (cb_internal_url, cb_internal_url)

        apache_conf += text_strip_margin('''
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
        |''')

    sudo('echo "%s" > /etc/apache2/sites-available/default' % apache_conf)


def _create_certs(common_name='127.0.0.1'):
    nonsecurekey = text_strip_margin('''
    |-----BEGIN RSA PRIVATE KEY-----
    |MIIEowIBAAKCAQEAtO4zZwNYOzux+ymvrW7kMojJ9diI7WxmPvESa1FNdY45TN5Z
    |WYSYcgYKDT/OuHDi9+49LlRPksV35scGNIJbqV9Cr4L0vHXfb9E9EdOIIkv3jOG9
    |QhhwIPxKrpJQP1hkPyxybWkH/IVHY06OxLIWPJO3NC74sQQvXZ2mMUoOW5KcQwiK
    |GfWf3mJKCccocNv3MXP4cb6ay7DQtbgQigjZaoQxffkJvq083h3y5lSQpnI56yBE
    |XHtHam8XCPnu7Axj0v5AGGaTYOa4RAzkG8PKpcvL8TRjPL3TMiiKJM2rQVrHdjcK
    |qBSOCr+fSNlr7E5KVBN8pfrsmly+NoflhA7hdQIDAQABAoIBAQCyz2rrlsmfGJsI
    |TyV48MwECV4XYt3IT0YpVFTQzPQRhvKoPmLtbna+0asjdvkVHTOitcevPtG5iwC5
    |id5fDKoMFMIx9OlsS837kz2YnYa/5nYLvJkvdjly0AP6zU0TnYbNTF72NEQZU5q+
    |0UeVqy8AxTfdEcLkJu+sxH4X3kmcQvhz2q7L2pbSgZ0JeL1Nfxmy0cjsSKEVy3qY
    |0tLVm4xHStoYNBpzgXyBqhz/wAhOcctUyl5qvpNzgR+ihASNRKYKIGcpjgjaSryk
    |0Gp8WmwrSuy1qQ8iqKRkSa5SSWqwl1umWlb1V8+7m4ic0A/GJEhzJ5pfXPMaOQuF
    |eHG60JNNAoGBAOyA1R1US5mjoaIZmahR2Rl6nYFQQy3HNqQy1AZU5hB4uTrMA2eW
    |sSxt1RMBjlE9C0sUOFB95w48/gZNI6JPdMFGgcux5WrndDruY8txiVl3rw2Dw7Ih
    |JMxNBsJRO0AZgijUm11HPBp/tJ4HjppZiqE0exjoNFGOLc/l4VOZ1PbDAoGBAMPY
    |j0dS7eHcsmu+v6EpxbRFwSyZG0eV51IiT0DFLfiSpsfmtHdA1ZQeqbVadM1WJSLu
    |ZJ8uvGNRnuLgz2vwKdI6kJFfWYZSS5jfnl874/OF6riNQDseX5CvB5zQvTFVmae+
    |Mld4x2NYFxQ1vIWnGITGQKhcZonBMyAjaQ9tAnNnAoGASvTOFpyX1VryKHEarSk7
    |uIKPFuP8Vq7z13iwkE0qGYBZnJP6ZENzZdRtmrd8hqzlPmdrLb+pkm6sSAz8xT2P
    |kI4rJwb74jT3NpJFmL4kPPHczli7lmJAymuDP+UE9VzgTtaLYzXni7J76TYV8T99
    |23fJp+w4YLzCMkj2cEuqHocCgYBb2KEBMwwqw4TNcOyP2XZFn/0DPF6FyPBuHXcL
    |ii2QCL68ux5hWv+O8n5mdaCXd9H8us5ntNRWw71+6y17kmsak6qe8peandekPyMX
    |yI+T8nbszBmWYB0zTlKEoYRIsbtY5qLXUOY5WeOg776U85NVGWDTVFomOnwOk2y+
    |9kGS+wKBgD3cL/zabIv/kK7KY84EdWdVH4sal3bRsiNn4ezj7go/ObMgR59O4Lr4
    |fYqT1igILotduz/knlkleY2fsqltStWYzRrG+/zNryIBco2+cIX8T120AnpbAvlP
    |gj0YVjuLJXSC9w/URFG+ZGg0kX0Koy1yS6fuxikiA4f5Lw9znjaD
    |-----END RSA PRIVATE KEY-----
    |''')
    file_write('nonsecure.key', nonsecurekey, sudo=True)
    sudo('openssl req -nodes -newkey rsa:2048 -keyout /tmp/nonsecure.key -out '
         '/tmp/server.csr -subj "/C=US/ST=TX/L=Austin/O=STACKOPS TECHNOLOGIES '
         'INC./OU=STACKOPS 360/CN=%s"' % common_name)
    sudo('openssl rsa -in /tmp/nonsecure.key -out /tmp/ssl.key')
    sudo('openssl x509 -req -days 365 -in /tmp/server.csr -signkey '
         '/tmp/ssl.key -out /tmp/ssl.crt')
    sudo('cp /tmp/ssl.crt /etc/ssl/certs/sslcert.crt')
    sudo('cp /tmp/ssl.key /etc/ssl/private/sslcert.key')


def _configure_apache_ssl(ec2_internal_url, compute_internal_url,
                          keystone_internal_url, glance_internal_url,
                          cinder_internal_url, quantum_internal_url,
                          portal_internal_url, activity_internal_url,
                          cb_internal_url, apache_conf=None):
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
    |''' % (ec2_internal_url, ec2_internal_url, compute_internal_url,
            compute_internal_url, keystone_internal_url,
            keystone_internal_url, glance_internal_url,
            glance_internal_url, cinder_internal_url, cinder_internal_url,
            quantum_internal_url, quantum_internal_url))

    if portal_internal_url is not None:
        apache_conf += text_strip_margin('''
        |
        |   ProxyPass /portal %s
        |   ProxyPassReverse /portal %s
        |
        ''') % (portal_internal_url, portal_internal_url)

    if activity_internal_url is not None:
        apache_conf += text_strip_margin('''
        |
        |   ProxyPass /activity %s
        |   ProxyPassReverse /activity %s
        |
        ''') % (activity_internal_url, activity_internal_url)

    if cb_internal_url is not None:
        apache_conf += text_strip_margin('''
        |
        |   ProxyPass /chargeback %s
        |   ProxyPassReverse /chargeback %s
        |
        ''') % (cb_internal_url, cb_internal_url)

    apache_conf += text_strip_margin('''
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
    |   BrowserMatch "MSIE [2-6]" nokeepalive ssl-unclean-shutdown %s
    |   # MSIE 7 and newer should be able to use keepalive
    |   BrowserMatch "MSIE [17-9]" ssl-unclean-shutdown
    |
    |</VirtualHost>
    |</IfModule>
    |''' % ("downgrade-1.0 force-response-1.0"))

    sudo('''echo '%s' > /etc/apache2/sites-available/default-ssl'''
         % apache_conf)


def configure_iptables(public_ip):
    package_ensure('iptables-persistent')
    sudo('service iptables-persistent flush')
    iptables_conf = text_strip_margin('''
    |
    |# Generated by iptables-save v1.4.4
    |*filter
    |:INPUT ACCEPT [0:0]
    |:FORWARD ACCEPT [0:0]
    |:OUTPUT ACCEPT [0:0]
    |-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
    |-A INPUT -d %s/32 -p tcp -m tcp --dport 80 -j ACCEPT
    |-A INPUT -d %s/32 -p tcp -m tcp --dport 6080 -j ACCEPT
    |-A INPUT -d %s/32 -p tcp -m tcp --dport 443 -j ACCEPT
    |-A INPUT -d %s/32 -p icmp -m icmp --icmp-type echo-request -j ACCEPT
    |-A INPUT -d %s/32 -j DROP
    |COMMIT
    |''' % (public_ip, public_ip, public_ip, public_ip, public_ip))
    sudo('echo "%s" > /etc/iptables/rules.v4' % iptables_conf)
    sudo('service iptables-persistent start')
