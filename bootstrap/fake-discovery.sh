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

# change /etc/hosts file to remove 127.0.1.1 and use the IP address of the node
set -x
NODE_NAME=$(hostname)
#NODE_IP=$(host $NODE_NAME | cut -d" " -f4)
#sed -i s/127.0.1.1/$NODE_IP/ /etc/hosts

#Add UseDNS setting it to NO in openshh-server
echo "UseDNS no" >> /etc/ssh/sshd_config

# Clean up apt sources
# /etc/apt/sources.list
sed -i /deb-src/d /etc/apt/sources.list
sed -i /#/d /etc/apt/sources.list
sed -i /^$/d /etc/apt/sources.list

mkdir /var/log/stackops
mkdir /etc/nova

echo "exit 0" >> /etc/rc.local

wget -q -O /etc/nova/STACKOPSVERSION http://mirror/ubuntu/setup/STACKOPSVERSION
wget -q -O /etc/nova/motd.stackops http://mirror/ubuntu/setup/motd.stackops

mkdir -p /root/.ssh
chmod 700 /root/.ssh
touch /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys

echo "blacklist vga16fb" >> /etc/modprobe.d/blacklist-framebuffer.conf
sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="quiet"/GRUB_CMDLINE_LINUX_DEFAULT="quiet elevator=noop"/g' /etc/default/grub
update-grub

wget -O - http://packages.stackops.net/stackops.gpg | apt-key add -
echo "deb http://mirror/ubuntu precise main" > /etc/apt/sources.list
echo "deb http://mirror/ubuntu precise extras" >>  /etc/apt/sources.list
apt-get update
apt-get -y --force-yes install stackops-agent

ln -s /var/lib/stackops/stackops.conf /etc/init/stackops.conf;
initctl reload-configuration

service stackops start

head=stackops-head
headport=3001

wget -N https://raw.github.com/StackOps/fabuloso/master/bootstrap/nc
wget -N https://raw.github.com/StackOps/fabuloso/master/bootstrap/lshw-static

chmod 755 nc
chmod 755 lshw-static

./lshw-static -xml > /tmp/hardware.xml
./nc -v -q2 $head $headport < /tmp/hardware.xml
