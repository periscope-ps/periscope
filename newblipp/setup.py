#!/usr/bin/env python
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

from setuptools import setup

version = "0.1.dev"

setup(
    name="blipp",
    version=version,
    packages=["blipp"],
    package_data={},
    author="Matthew Jaffee",
    author_email="matthew.jaffee@gmail.com",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    url="https://github.com/periscope-ps/periscope",
    
    install_requires=[
        "requests",
        "netlogger>=4.3.0",
        "ethtool",
    ],
    dependency_links=[
        "http://129.79.244.8/python-ethtool-0.7.tar#egg=ethtool-0.7",
    ],
    entry_points = {
        'console_scripts': [
            'blippd = blipp.sched:main',
        ]
    },
)
