#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'intelligentguy'


#from distutils.core import setup
from setuptools import setup

setup(
        # Application name:
        name="pyPrivnote",
        # Version number (initial):
        version="0.0.1a1",
        # Application author details:
        author="Gleb Zaripov",
        author_email="gleb-zaripov@yandex.ru",
        # license:
        license='GPLv3+',
        classifiers=[
            'Development Status :: 3 - Alpha',  # 3 - Alpha, 4 - Beta, 5 - Production/Stable
            # Indicate who your project is intended for
            "Intended Audience :: Customer Service",
            "Intended Audience :: Developers",
            "Intended Audience :: Other Audience",
            "Intended Audience :: Science/Research",
            # Pick your license as you wish (should match "license" above)
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Operating System :: Unix',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: MacOS :: MacOS X',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Topic :: Communications',
            'Topic :: Software Development :: Libraries',
            'Topic :: Software Development :: Build Tools',
            "Topic :: Software Development :: Version Control :: Git",
            "Topic :: Security :: Cryptography",
        ],
        keywords='privnote priv note pyprivnote notes cryptography private message self-destroy self-destruct',
        # Packages
        packages=["pyPrivnote"],
        # Include additional files into the package
        include_package_data=True,
        # Details
        url="http://pypi.python.org/pypi/pyPrivnote/",
        #
        description="A Python Interface to Privnote service",
        long_description=open("README.md").read(),
        # Dependent packages (distributions)
        install_requires=[
            "pycryptodome",
            "requests",
        ]
)
