# -*- coding: utf-8 -*-
"""setup script for building, distributing and installing."""
from os import path

from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

setup(
    name='ImageCrypt',

    version='0.1.0',

    description='Image LSB and DCT steganography cli tool.',

    url='https://github.com/rszamszur/ImageCrypt',

    author='Radosław Szamszur',
    author_email='radoslawszamszur@gmai.com',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Cryptography Tools',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    packages=find_packages(),

    install_requires=[
        'click>=6.6',
        'six>=1.11.0',
    ],

    entry_points={
        'console_scripts': ['ImageCrypt=ImageCrypt.cli.cli:cli'],
    },
)
