#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0',
                'sanic',
                'sanic-jwt',
                'asynqp>=0.5.1']

setup_requirements = []

test_requirements = []

setup(
    author="Man QuanXing",
    author_email='manquanxing@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="SAM V1 Events Output Api Server",
    entry_points={
        'console_scripts': [
            'sam-events=events.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='events',
    name='events',
    packages=find_packages(include=['events']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/manqx/events',
    version='0.1.0',
    zip_safe=False,
)
