# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from setuptools import setup, find_packages
from os import path
from io import open


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Djtools',
    version='0.2',
    description='Tools for reading and writing DJ software media libraries.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/xa4a/djtools',
    author='Ievgen Varavva',
    author_email='yvaravva@google.com',
    classifiers=[
       "Development Status :: 3 - Alpha",
       "Intended Audience :: Developers",
       "Intended Audience :: End Users/Desktop",
       "Topic :: Multimedia :: Sound/Audio :: Analysis",
       "Topic :: Multimedia :: Sound/Audio :: Editors",
       "License :: OSI Approved :: Apache Software License",
       "Programming Language :: Python :: 3.6",
    ],
    keywords='dj djay rekordbox cue points',
    packages=find_packages(exclude=['tests']),
    license='Apache License 2.0',
    install_requires=[
        'bpylist2==2.0.1',
        'dataclasses',
    ],
    extras_require={
        'test': ['nose'],
    },
    python_requires='>=3.0',
    test_suite='nose.collector',
    tests_require=['nose'],
)
