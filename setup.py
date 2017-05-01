#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import (
    setup,
    find_packages,
)


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-pypom-navigation',
    version='0.0.1',
    author='Tierra QA team',
    author_email='DLQA@tierratelematics.com',
    maintainer='Tierra QA team',
    maintainer_email='DLQA@tierratelematics.com',
    license='Apache Software License 2.0',
    url='https://github.com/tierratelematics/pytest-pypom-navigation',
    description='Core engine for tierra_qa package',
    long_description=read('README.rst'),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'pytest>=3.0.7',
        'pypom_form',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points={
        'pytest11': [
            'pypom-navigation = pypom_navigation.plugin',
        ],
    },
)