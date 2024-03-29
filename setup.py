#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


base_dir = os.path.dirname(os.path.abspath(__file__))

def get_version(filename="pysugarcrm/__init__.py"):
    with open(os.path.join(base_dir, filename), encoding="utf-8") as initfile:
        for line in initfile.readlines():
            m = re.match("__version__ *= *['\"](.*)['\"]", line)
            if m:
                return m.group(1)

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    "requests>=2.7.0",
]

test_requirements = [
    "responses>=0.4.0",
]

setup(
    name='pysugarcrm',
    version=get_version(),
    description="API Wrapper for SugarCRM v10",
    long_description=readme + '\n\n' + history,
    author="Diego Navarro",
    author_email='diego@feverup.com',
    url='https://github.com/Feverup/pysugarcrm',
    packages=[
        'pysugarcrm',
    ],
    package_dir={'pysugarcrm':
                 'pysugarcrm'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='pysugarcrm',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
