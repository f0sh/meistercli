#!/usr/bin/env python
from setuptools import find_packages, setup


setup(
    name='meistercli',
    version='0.0.1',
    description='MeisterCLI',
    long_description='MeisterTask CLI',
    url='https://github.com/fstaubach/meistercli',
    maintainer='Florian Staubach',
    maintainer_email='',
    platforms=['any'],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    python_requires='>=3.5',
    install_requires=['pymeistertask>=0.1.2', 'click>=8.1.3', 'tabulate>=0.9.0'],
    entry_points={"console_scripts": ["meistercli=meistercli.meistercli:main"]},
    license='GPL',
)
