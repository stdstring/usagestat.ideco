#! /usr/bin/python

# if we use unicode, then we will receive following error: "TypeError: 'package' must be a string (dot-separated), list, or tuple"
#from __future__ import unicode_literals
from setuptools import setup, find_packages

PRODUCT_VERSION = '1.0.b1'
AUTHOR='Andrey Ushakov'
AUTHOR_EMAIL='a_ushakov@ideco.ru'
EXCLUDE_FILTER = ['tests', 'tests.*']

# stat_source_common
src = 'stat_source_common'
setup(name='stat_source_common',
    version=PRODUCT_VERSION,
    description='Common lib for all sources of usage statistics',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    # packages
    package_dir = {'': src},
    packages = find_packages(src, exclude=EXCLUDE_FILTER),
    # requirements
    requires=[])

# stat_file_source
src = 'stat_file_source'
setup(name='stat_file_source',
    version=PRODUCT_VERSION,
    description='Base lib for file sources',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    # packages
    package_dir = {'': src},
    packages = find_packages(src, exclude=EXCLUDE_FILTER),
    # requirements
    requires=[])

# stat_db_source
src = 'stat_db_source'
setup(name='stat_db_source',
    version=PRODUCT_VERSION,
    description='Base lib for db sources',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    # packages
    package_dir = {'': src},
    packages = find_packages(src, exclude=EXCLUDE_FILTER),
    # requirements
    requires=[])

# stat_ics_conf_collector
src = 'stat_ics_conf_collector'
setup(name='stat_ics_conf_collector',
    version=PRODUCT_VERSION,
    description='App for collecting data from ics.conf file',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    # packages
    package_dir = {'': src},
    packages = find_packages(src, exclude=EXCLUDE_FILTER),
    # entry_point
    entry_points = {'console_scripts': ['stat_ics_conf_collector = stat_ics_conf_collector.collector_entry_point:execute']},
    # requirements
    requires=[])

# stat_ics_db_collector
src = 'stat_ics_db_collector'
setup(name='stat_ics_db_collector',
    version=PRODUCT_VERSION,
    description='App for collecting data from ics_main database (ics_main.gdb)',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    # packages
    package_dir = {'': src},
    packages = find_packages(src, exclude=EXCLUDE_FILTER),
    # entry_point
    entry_points = {'console_scripts': ['stat_ics_db_collector = stat_ics_db_collector.collector_entry_point:execute']},
    # requirements
    requires=['kinterbasdb'])

# stat_sender
src = 'stat_sender'
setup(name='stat_sender',
    version=PRODUCT_VERSION,
    description='App for sending collected data to the server',
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    # packages
    package_dir = {'': src},
    packages = find_packages(src, exclude=EXCLUDE_FILTER),
    # entry_point
    entry_points = {'console_scripts': ['stat_sender = stat_sender.stat_sender_entry_point:execute']},
    # requirements
    requires=[])

__author__ = 'andrey.ushakov'
