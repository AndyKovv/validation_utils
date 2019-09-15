!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()


setup_requirements = ['pytest-runner', ]
test_requirements = ['pytest', ]


setup(
    author="Andrii Kovalov",
    author_email='andy.kovv@gmail.com',
    classifiers=[
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Validation utils library",
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    keywords='validation_utils',
    name='validation_utils',
    packages=find_packages(include=['validation_utils']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    version='0.0.1',
    zip_safe=False,
)
