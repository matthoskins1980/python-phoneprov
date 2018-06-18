#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='phoneprov',
    version="2.0",
    description="NPG's Phone Provisioning system",
    author='Matt Hoskins',
    author_email='matt.hoskins@npgco.com',
    url='https://www.npgco.com',
    packages=find_packages(exclude=['',]),
    install_requires=[
        'sqlalchemy',
        'sqlalchemy_utils',
        'psycopg2-binary',
        'ldap3',
        'jinja2',
        'requests',
        'simplejson',
        'fbtftp'
    ]
)

