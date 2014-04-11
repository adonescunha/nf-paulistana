#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Nota Fiscal Paulistana
# https://github.com/adonescunha/nf-paulistana

# Licensed under the MIT license:
# http://www.opensource.org/licenses/mit-license
# Copyright (c) 2014 Adones Cunha adonescunha@gmail.com


from setuptools import setup

from nf_paulistana import version


setup(
    name='nf-paulistana',
    version=version.to_str(),
    description=u'Emissão de lotes RPS.',
    author='Adones Cunha',
    author_email='adonescunha@gmail.com',
    url='https://github.com/adonescunha/nf-paulistana',
    packages=[
        'nf_paulistana'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
