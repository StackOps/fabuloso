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
from fabric.api import sudo, puts, env, local, run, abort
from cuisine import group_ensure, user_ensure, upstart_ensure, \
    package_ensure
from cuisine import re, os

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

OS_VERSIONS_SUPPORTED = ['3.2.0-26-generic #41-Ubuntu',
                         '3.2.0-26-generic #41-Ubuntu']


def _configureInterfacesFile(bond_name, bond_slaves, bond_options):
    interfaces = sudo('cat "/etc/network/interfaces"')
    puts(interfaces)

    # Search for previous conf of any slave
    reuse_iface = None
    for slave in bond_slaves:
        puts(slave)
        if re.search(r'^[ \t]*iface[ \t]+%s' % (re.escape(slave)), interfaces,
                     re.M):
            reuse_iface = slave
            break
    puts('reuse_iface = %s' % reuse_iface)

    if reuse_iface:
        # Convert slave to bond
        interfaces = re.sub(
            r'(^[ \t]*iface[ \t]+)%s([ \t]+.*$)' % re.escape(reuse_iface),
            r'\1%s\2\n\t%s\n\tbond-slaves none' % (
                bond_name,
                '\n\t'.join(('bond-'+' '.join(o.split('=', 1))
                             for o in bond_options.split()))),
            interfaces,
            count=1,
            flags=re.M | re.I
        )
        interfaces = re.sub(
            (r'(^[ \t]*auto[ \t+](?:[^ \t]+[ \t]+)?)%s([ \t]?.*$)' %
                re.escape(reuse_iface)),
            r'\1%s\2' % bond_name,
            interfaces,
            flags=re.M | re.I
        )
    else:
        # Create bond interface
        interfaces = '\n'.join((
            interfaces,
            'auto %s' % bond_name,
            'iface %s inet manual' % bond_name,
            '\tbond-slaves none',
            '\n'.join(('\tbond-'+' '.join(o.split('=', 1))
                      for o in bond_options.split()))))

    # Remove previous slave conf
    for slave in bond_slaves:
        iface_match = re.search(r'^[ \t]*iface[ \t]+%s(?:[ \t]|$)' %
                                re.escape(slave), interfaces, re.M)
        if not iface_match:
            continue
        iface_start = iface_match.start()
        next_match = re.search(r'^[ \t]*(?:iface|mapping|auto|allow-|source)',
                               interfaces[iface_match.end():], re.M)
        if next_match:
            iface_end = iface_start + next_match.end()
        else:
            iface_end = len(interfaces)
        interfaces = interfaces[:iface_start] + interfaces[iface_end:]

    def _clean_auto(line):
        parts = line.split()
        if not parts or parts[0] != 'auto':
            return line
        parts = [p for p in parts[1:] if p not in bond_slaves]
        if not parts:
            return ''
        return 'auto %s\n' % ' '.join(parts)

    interfaces = ''.join(map(_clean_auto, StringIO(interfaces)))

    # Create slaves
    for slave in bond_slaves:
        conf = """
    auto %(slave)s
    iface %(slave)s inet manual
        bond-master %(bond)s
        bond-primary %(slaves)s
        up ifconfig $IFACE up
    """
        conf = conf % {'bond': bond_name, 'slave': slave,
                       'slaves': ' '.join(bond_slaves)}
        interfaces = ''.join((interfaces, conf))

    puts(interfaces)
    sudo('echo "%s" > /etc/network/interfaces' % interfaces)


def _bits2netmask(bits):
    bits = int(bits)
    parts = []
    while bits > 0:
        if bits > 7:
            parts.append('255')
        else:
            parts.append(str((255 ^ 2 ** (8-bits)) + 1))
        bits -= 8
    if len(parts) < 4:
        parts.extend(['0']*(4-len(parts)))
    return '.'.join(parts)


def _get_ip_info(interface=''):
    line = sudo('ip -f inet -o addr show %s' % interface).split()
    if not line:
        return None
    order, name = line[0:2]
    ip, netmask = line[3].split('/')
    return {'id': int(order[:-1]), 'name': name, 'ip': ip,
            'netmask': _bits2netmask(netmask),
            'broadcast': line[5]}


def _configureOnline(bond_name, bond_slaves, bond_options):
    sudo('modprobe bonding %s' % bond_options)
    ip_info = None
    for slave in bond_slaves:
        puts(slave)
        ip_info = _get_ip_info(slave)
        if ip_info:
            break
    if ip_info:
        sudo('ifconfig %s %s netmask %s' % (bond_name, ip_info['ip'],
                                            ip_info['netmask']))
    else:
        sudo('ifconfig %s up' % bond_name)
    for slave in bond_slaves:
        sudo('ifconfig %s up' % slave)
    sudo('ifenslave %s %s' % (bond_name, ' '.join(bond_slaves)))


def vagrant():
    # change from the default user to 'vagrant'
    env.user = 'vagrant'
    # connect to the port-forwarded ssh
    env.hosts = ['127.0.0.1:2222']

    # use vagrant ssh key
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1]


def check_base_os():
    """Check if the base Operating System is supported"""
    version = run('uname -a')
    for v in OS_VERSIONS_SUPPORTED:
        if not v in version:
            puts('%s supported' % version)
            return
    abort('The %s Operating System is not supported! Process stopped!' %
          version)


def hostname():
    """Returns current hostname"""
    run('hostname')


def no_framebuffer():
    """Disable vga16fb framebuffer to boost virtual console"""
    sudo('sed -i /vga16fb/d /etc/modprobe.d/blacklist-framebuffer.conf ')
    sudo("""echo "blacklist vga16fb" >>
            /etc/modprobe.d/blacklist-framebuffer.conf""")


def change_hostname(hostname):
    """Modify the hostname of the server"""
    current_hostname = run('hostname')
    sudo('echo "%s" > /etc/hostname' % hostname)
    sudo("sed -i 's/%s/%s/g' /etc/hosts" % (current_hostname, hostname))
    sudo("hostname %s" % hostname)


def add_nova_user():
    """Add nova and glance users and groups if they don't exists in the
       operating system"""
    group_ensure('nova', 201)
    user_ensure('nova', home='/var/lib/nova', uid=201, gid=201,
                shell='/bin/false')


def add_glance_user():
    """Add nova and glance users and groups if they don't exists in the
       operating system"""
    group_ensure('glance', 202)
    user_ensure('glance', home='/var/lib/glance', uid=202, gid=202,
                shell='/bin/false')


def configure_ntp(ntpHost):
    """Change default ntp server to client choice"""
    sudo("sed -i 's/server ntp.ubuntu.com/server %s/g' /etc/ntp.conf" %
         ntpHost)
    sudo("service ntp stop")
    sudo("ntpdate -u %s" % ntpHost)
    upstart_ensure('ntp')


def remove_repos():
    """Remove existing repositories and updates"""
    sudo('sed -i /precise-updates/d /etc/apt/sources.list')
    sudo('sed -i /precise-security/d /etc/apt/sources.list')
    sudo('sed -i /archive.ubuntu.com/d /etc/apt/sources.list')
    sudo('rm  -f /etc/apt/sources.list.d/stackops.list')
    sudo('apt-get -y update')


def add_repos():
    """Clean and Add necessary repositories and updates"""
    sudo('sed -i /precise-updates/d /etc/apt/sources.list')
    sudo('sed -i /precise-security/d /etc/apt/sources.list')
    sudo('sed -i /archive.ubuntu.com/d /etc/apt/sources.list')
    sudo('rm -f /etc/apt/sources.list.d/stackops.list')
    sudo('echo "deb http://us.archive.ubuntu.com/ubuntu/ precise main '
         'universe" >> /etc/apt/sources.list')
    sudo('echo "deb http://us.archive.ubuntu.com/ubuntu/ precise-security '
         'main universe" >> /etc/apt/sources.list')
    sudo('echo "deb http://us.archive.ubuntu.com/ubuntu/ precise-updates '
         'main universe" >> /etc/apt/sources.list')
    sudo('wget -O - http://repos.stackops.net/keys/stackopskey_pub.gpg '
         '| apt-key add -')
    sudo('echo "deb http://repos.stackops.net/ folsom-dev main" >> '
         '/etc/apt/sources.list.d/stackops.list')
    sudo('echo "deb http://repos.stackops.net/ precise-dev main" '
         '>> /etc/apt/sources.list.d/stackops.list')
    sudo('apt-get -y update')


def configure_bond(bond_name=None, bond_slaves=None, bond_options='mode 1'):
    """Configure bond in the existing system"""
    package_ensure('ifenslave')
    slaves = bond_slaves.split()
    _configureInterfacesFile(bond_name, slaves, bond_options)
    _configureOnline(bond_name, slaves, bond_options)


def add_iface(iface=None, dhcp=False, gateway=None):
    """Update /etc/network/interfaces with info for the current scheme"""
    fp = ""
    fp = """auto lo
    iface lo inet loopback

"""
    for i in iface_list():
        iface = _get_ip_info(i)
        puts(iface)
        if iface:
            # Write the entry for the new interface
            fp += """auto %s""" % (iface['name'])
            if dhcp:
                fp += """
    iface %s inet dhcp""" % (iface['name'])
            else:
                fp += """
    iface %s inet static""" % (iface['name'])
                if iface['ip']:
                    fp += """
    address %s""" % iface['ip']
                if iface['netmask']:
                    fp += """
    netmask %s""" % iface['netmask']
                if iface['broadcast']:
                    fp += """
    broadcast %s""" % iface['broadcast']
                if gateway:
                    fp += """
    gateway %s""" % iface['gateway']

            puts(fp)


def cpu():
    cpu = sudo("cat /proc/cpuinfo | grep 'model name' | sed 's/\(.*\): \
               //g'").splitlines()
    puts(cpu)
    return cpu


def cpu_count():
    count = len(cpu())
    puts(count)
    return count


def cpu_speed():
    speed = sudo("cat /proc/cpuinfo | grep 'cpu MHz' | sed \
                 's/[^0-9\.]//g'").splitlines()
    puts(speed)
    return speed


def memory():
    mem = 1024 * int(sudo("cat /proc/meminfo | grep 'MemTotal' | sed \
                          's/[^0-9\.]//g'"))
    puts(mem)
    return mem


def is_virtual():
    virt = sudo("egrep '(vmx|svm)' /proc/cpuinfo")
    if len(virt) > 0:
        return "True"
    else:
        return "False"


def iface_list():
    ifaces = sudo("cat /proc/net/dev | sed 's/:\(.*\)//g'").splitlines()
    del ifaces[0]
    del ifaces[0]
    ifaces_list = []
    for x in ifaces:
        y = x.strip()
        if ((y != "lo")
                and not(y.startswith("vir"))
                and not(y.startswith("br"))
                and not(y.startswith("vnet"))
                and not(y.startswith("pan"))):
            ifaces_list.append(y)
    puts(ifaces_list)
    return ifaces_list


def iface_vendor(iface):
    tmp = sudo("lshw -short -c network | grep '%s'" % iface).splitlines()
    vendor = tmp[len(tmp)-1][43:]
    puts(vendor)
    return vendor


def mounts():
    mnt = sudo("mount -v")
    lines = mnt.split('\n')
    inf = []
    for line in lines:
        dev = {}
        device = line.split()[0]
        mountpoint = line.split()[2]
        if (device != "none"):
            dev['mountpoint'] = mountpoint
            dev['device'] = device
            try:
                s = os.statvfs(line.split()[2])
                dev['size'] = s.f_bsize * s.f_blocks
                dev['used'] = s.f_bsize * (s.f_blocks - s.f_bavail)
            except OSError:
                print 'OSError'
            inf.append(dev)
    puts(inf)
    return inf


def block_devices():
    procfile = sudo("cat /proc/partitions").splitlines()
    procfile.pop(0)
    procfile.pop(0)
    parts = [p.split() for p in procfile]

    mnt = sudo("mount -v").split('\n')
    mounts = [p.split() for p in mnt]
    mountvalid = {}
    for p in mounts:
        if (p[0] != 'none'):
            mountvalid[p[0]] = p
    inf = []
    for device in parts:
        dev = {}
        if ('/dev/'+device[3] in mountvalid):
            dev['mountpoint'] = mountvalid['/dev/'+device[3]][2]
            try:
                s = os.statvfs(dev['mountpoint'])
                dev['size'] = s.f_bsize * s.f_blocks
                dev['used'] = s.f_bsize * (s.f_blocks - s.f_bavail)
            except OSError:
                print 'OSError'
        else:
            dev['mountpoint'] = ''
            dev['size'] = int(device[2]) * 1024
            dev['used'] = -1
        dev['device'] = '/dev/'+device[3]
        inf.append(dev)
    puts(inf)
    return inf


def nameservers():
    mnt = sudo("cat /etc/resolv.conf")
    lines = mnt.splitlines()
    inf = []
    for line in lines:
        if line.startswith("nameserver"):
            inf.append({'nameserver': line.split(" ")[1]})
    puts(inf)
    return inf


def network_config():
    def getDhcpInfo(device):
        info = {'address': 'none', 'netmask': 'none', 'gateway': 'none'}
        mnt = sudo('LC_ALL=c ifconfig '+device)
        match = re.search(r'inet addr:(\S+).*mask:(\S+)', mnt, re.I)
        if match:
            info['address'] = match.group(1)
            info['netmask'] = match.group(2)
        mnt = sudo('route -n ')
        match = re.search(r'^0.0.0.0\s+(\S+).*'+re.escape(device),
                          mnt, re.I | re.M)
        if match:
            info['gateway'] = match.group(1)
        return info
    inf = []
    mnt = sudo('cat /etc/network/interfaces | egrep -v "^s*(#|$)"')
    devnets = mnt.split('auto')
    for devnet in devnets:
        if len(devnet) > 0:
            net = devnet.splitlines()
            dev = {}
            element = net[0].strip()
            if element in iface_list():
                dev['name'] = element
                dev['dhcp'] = "true"
                dev['address'] = "none"
                dev['netmask'] = "none"
                dev['gateway'] = "none"
                dev['default'] = "false"
                dev['virtual'] = "false"
                dev['bond-mode'] = "none"
                dev['bond-miimon'] = "none"
                dev['bond-master'] = "none"
                for e in net:
                    params = e.strip().split(' ')
                    if params[len(params)-1] == 'dhcp':
                        dev['dhcp'] = "true"
                    if params[len(params)-1] == 'static':
                        dev['dhcp'] = "false"
                    if params[0] == 'address':
                        dev['address'] = params[1]
                    if params[0] == 'netmask':
                        dev['netmask'] = params[1]
                    if params[0] == 'gateway':
                        dev['gateway'] = params[1]
                    if params[0] == 'bridge_ports':
                        dev['virtual'] = "true"
                    if params[0] == 'bond-mode':
                        dev['bond-mode'] = params[1]
                    if params[0] == 'bond-miimon':
                        dev['bond-miimon'] = params[1]
                    if params[0] == 'bond-master':
                        dev['bond-master'] = params[1]
                if dev['dhcp'] == 'true':
                    dev.update(getDhcpInfo(dev['name']))
            if len(dev) > 0:
                inf.append(dev)
    puts(inf)
    return inf


def add_host(hostname, ip):
    sudo('sed -i /%s/d /etc/hosts' % hostname)
    sudo('echo "%s  %s" >> /etc/hosts' % (hostname, ip))


def remove_host(hostname):
    sudo('sed -i /%s/d /etc/hosts' % hostname)


def show_partitions(disk=None):
    out = sudo("""for hdd in `ls %s`;do  parted -s -m $hdd unit MB
               print ;done """ % disk)
    puts(out)
    return out


def parted(disk='/dev/sdb', start=0, end=100):
    sudo('parted -s %s mklabel msdos' % disk)
    sudo('parted -s %s unit %% mkpart primary %s%% %s%%' % (disk, start, end))


def execute_bootstrap():
    boot = "https://raw.github.com/StackOps/fabuloso/master/bootstrap/init.sh"
    run("wget -O - " + boot + " | sudo sh")
