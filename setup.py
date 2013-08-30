#!/usr/bin/python
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
import glob
import os
import setuptools
import subprocess
import sys
import unittest

requirements = ['pep8', 'cuisine', 'pyyaml', 'setuptools',
                'python-keystoneclient', 'MySQL-python', 'pika ',
                'expects>=0.1,<0.2']

if sys.version_info < (2, 7):
    requirements.append('argparse')
elif sys.version_info < (2, 6):
    raise 'Must use python 2.6 or greater'


class TestCommand(setuptools.Command):

    description = "run tests"
    user_options = []
    test_directory = "fabuloso/test"

    def initialize_options(self):
        """Loads the current directory into classpath.

        Loads the current directory in the classpath. Look at libclouds
        way to do it:
        https://github.com/apache/libcloud/blob/trunk/setup.py#L72
        """
        THIS_DIR = os.path.abspath(os.path.split(__file__)[0])
        sys.path.insert(0, THIS_DIR)
        sys.path.insert(0, os.path.join(THIS_DIR, self.test_directory))
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        """Run all test files.

        Puts all the files into the directory 'fabuloso/test' those name are
        test_* as test to be runned.
        """
        testfiles = []
        for t in glob.glob(os.path.join(self._dir, self.test_directory,
                                        'test_*.py')):
            testfiles.append('.'.join([self.test_directory.replace('/', '.'),
                                      os.path.splitext(
                                          os.path.basename(t))[0]]))

        tests = unittest.TestLoader().loadTestsFromNames(testfiles)

        t = unittest.TextTestRunner(verbosity=2)
        res = t.run(tests)
        sys.exit(not res.wasSuccessful())


class Pep8Command(setuptools.Command):

    description = "run pep8 command"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            import pep8
            pep8
        except ImportError:
            print('Missing "pep8" library. You can install it using pip: '
                  'pip install pep8')
            sys.exit(1)

        cwd = os.getcwd()
        retcode = subprocess.call(('pep8 %s/fabuloso/' % (cwd)).split(' '))
        sys.exit(retcode)


setuptools.setup(name='fabuloso',
                 packages=['fabuloso'],
                 package_data={'fabuloso': ['data/easter_egg.txt',
                                            'catalog/*/*.*']},
                 author='Jaume Devesa',
                 author_email='jaume.devesa@stackops.com',
                 description='StackOps remote executor',
                 install_requires=requirements,
                 entry_points={
                     'console_scripts': [
                         'fabuloso = fabuloso.main:main',
                         'fabulosamente = fabuloso.main:ee'
                     ]
                 },
                 data_files=[
                     (os.path.join(os.path.expanduser('~'),
                                   '.config/fabuloso'),
                      ['fabuloso/data/config.py'])
                 ],
                 version='0.1',
                 license='Apache License 2.0',
                 cmdclass={
                     'test': TestCommand,
                     'pep8': Pep8Command
                 },
                 classifiers=[
                     "Development Status :: 2 - Pre-Alpha",
                     "Environment :: Console",
                     "Intended Audience :: Developers",
                     "Intended Audience :: Information Technology",
                     "License :: OSI Approved :: Apache Software License",
                     "Natural Language :: English",
                     "Operating System :: POSIX :: Linux",
                     "Programming Language :: Python",
                     "Programming Language :: Python :: 2",
                     "Programming Language :: Python :: 2.7",
                     "Topic :: System"
                 ])
