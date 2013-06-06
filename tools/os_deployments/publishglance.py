#!/usr/bin/env python
#   Copyright 2011-2012 STACKOPS TECHNOLOGIES S.L.
#
# Interactive shell based on Django:
#
# Copyright (c) 2005, the Lawrence Journal-World
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     1. Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#
#     2. Redistributions in binary form must reproduce the above copyright
#        notice, this list of conditions and the following disclaimer in the
#        documentation and/or other materials provided with the distribution.
#
#     3. Neither the name of Django nor the names of its contributors may be
#        used to endorse or promote products derived from this software without
#        specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""
  CLI interface for VPC management.
"""
import getopt

import gettext
import glob
import os
import sys
import json
import subprocess
import uuid

MINIMUM_ROOT_SIZE_GB = '2'
VERBOSE=False

def execute(cmd):
    if VERBOSE:
        print cmd
    env = os.environ.copy()
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env=env)
    stdout_text, stderr_text = p.communicate()
    if stderr_text is not None and len(stderr_text) > 0:
        print stderr_text
    return stdout_text, stderr_text


def exists(keystone, username, tenant, password, infile):
    image_name = os.path.basename(infile)
    cmd = 'glance --os-username %s --os-password %s --os-tenant-name %s --os-auth-url %s details | grep "%s"' % (
        username, password, tenant, keystone, image_name)
    (stdout, stderr) = execute(cmd)
    print "Checking if image %s exists..." % image_name
    ex = len(stdout.strip(' \t\n\r')) > 0
    return ex


def publish(keystone, username, tenant, password, folder, public):
    """Publish the selected image for the tenant"""
    credentials = '--os_username=%s --os_password=%s --os_tenant_name=%s --os_auth_url=%s' % (
    username, password, tenant, keystone)
    for infile in glob.glob(os.path.join(folder, '*.tar.gz')):
        full_folder_path = '%s/%s' % ('/tmp', uuid.uuid1())
        os.makedirs(full_folder_path)
        execute('tar xfz %s -C %s' % (infile, full_folder_path))
        (stdout, stderr) = execute('find %s -name "*.img"' % full_folder_path)
        image_file = stdout.strip()
        image_name = os.path.basename(image_file)
        (stdout, stderr) = execute('find %s \( -name "*-kernel" -o -name "*-vmlinuz*" \)' % full_folder_path)
        kernel_file = stdout.strip()
        kernel_name = os.path.basename(kernel_file)
        (stdout, stderr) = execute('find %s -name "*-initrd"' % full_folder_path)
        ramdisk_file = stdout.strip()
        if len(ramdisk_file)>0:
            ramdisk_name = os.path.basename(ramdisk_file)
        else:
            ramdisk_name = None
        if not exists(keystone, username, tenant, password, kernel_name):
            print('Uploading image %s' % image_name)
        #                execute('qemu-img resize %s %sG' % (image_file, MINIMUM_ROOT_SIZE_GB))
            if ramdisk_name:
                (stdout, stderr) = execute(
                    'glance %s add name="%s" is_public=%s container_format=ari disk_format=ari < %s' % (
                        credentials, ramdisk_name, public, ramdisk_file))
                (ramdisk_id, stderr) = execute('echo "%s" | cut -d":" -f2 | tr -d " "' % stdout)
            else:
                ramdisk_id = None
            (stdout, stderr) = execute(
                'glance %s add name="%s" is_public=%s container_format=aki disk_format=aki < %s' % (
                credentials, kernel_name, public, kernel_file))
            (kernel_id, stderr) = execute('echo "%s" | cut -d":" -f2 | tr -d " "' % stdout)
            if ramdisk_id:
                execute(
                    'glance %s add name="%s" is_public=%s container_format=ami disk_format=ami ramdisk_id=%s kernel_id=%s < %s' % (
                        credentials, image_name, public, ramdisk_id.strip(' \t\n\r'), kernel_id.strip(' \t\n\r'), image_file))
            else:
                execute(
                    'glance %s add name="%s" is_public=%s container_format=ami disk_format=ami kernel_id=%s < %s' % (
                        credentials, image_name, public, kernel_id.strip(' \t\n\r'), image_file))
            print('Uploaded image %s' % image_name)
        execute('rm -fR %s' % full_folder_path)
    try:
        for infile in glob.glob(os.path.join(folder, '*.qcow2')):
            image_name = os.path.basename(infile)
            if not exists(keystone, username, tenant, password, image_name):
                print('Uploading image %s' % image_name)
                (stdout, stderr) = execute('glance %s add name="%s" is_public=%s container_format=bare disk_format=qcow2 < %s' % (credentials, image_name, public, infile))
                print 'Uploaded image %s' % image_name
        for infile in glob.glob(os.path.join(folder, '*.img')):
            image_name = os.path.basename(infile)
            if not exists(keystone, username, tenant, password, image_name):
                print('Uploading image %s' % image_name)
                (stdout, stderr) = execute('glance %s add name="%s" is_public=%s container_format=bare disk_format=raw < %s' % (credentials, image_name, public, infile))
                print 'Uploaded image %s' % image_name
    except Exception as e:
        print 'ERROR:' + e.__str__()
        return

def usage():
    print "This is how it works"
    return

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "v:k:u:t:p:x:f:", ["verbose=", "keystone=", "username=", "tenant=", "password=", "ispublic=", "folder="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    public = False
    folder = '.'
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-v", "--verbose"):
            VERBOSE = True
        elif opt in ("-k", "--keystone"):
            keystone = arg
        elif opt in ("-u", "--username"):
            username = arg
        elif opt in ("-t", "--tenant"):
            tenant = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-x", "--ispublic"):
            public = arg == 'true'
        elif opt in ("-f", "--folder"):
            folder = arg
    publish(keystone, username, tenant, password, folder, public)
    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])

