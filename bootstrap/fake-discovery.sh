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

echo "deb http://mirror/ubuntu precise main" > /etc/apt/sources.list
echo "deb http://mirror/ubuntu precise extras" >>  /etc/apt/sources.list
apt-get update
apt-get -y --force-yes install stackops-agent

head=stackops-head
headport=3001

wget -N https://raw.github.com/StackOps/fabuloso/master/bootstrap/nc
wget -N https://raw.github.com/StackOps/fabuloso/master/bootstrap/lshw-static

chmod 755 nc
chmod 755 lshw-static

./lshw-static -xml > /tmp/hardware.xml
./nc -v -q2 $head $headport < /tmp/hardware.xml
