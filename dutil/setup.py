#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2012 Zhang ZY<http://idupx.blogspot.com/>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import distutils.core
import os
import sys


def _setup():
    kwargs = {}

    # Importing setuptools adds some features like "setup.py develop", but
    # it's optional so swallow the error if it's not there.
    try:
        import setuptools
    except ImportError as e:
        print(e)
        os._exit(1)

    distutils.core.setup(
        name="dutil",
        version="1.0.8",
        author="daling_qa",
        author_email="qa.list@daling.com",
        url="http://qa.corp.daling.com",
        description="tools",
        packages=setuptools.find_packages(exclude=["test", "*.log"]),
        package_data={
        },
        entry_points={
         'console_scripts': [
         ],
          },
        install_requires=[
            'pytest',
            'pyyaml',
            'records'
        ],
        **kwargs
    )


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == 'publish':
            os.system('make publish')
            sys.exit()

    _setup()


if __name__ == '__main__':
    main()
