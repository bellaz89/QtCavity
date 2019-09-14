#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name='QtCavity',
    version='1.0',
    packages=find_packages(),
    package_data={'' : ['LICENSE.md'], 'qtcavity': ['resources/*.ui']},
    entry_points={ 'gui_scripts': ['qtcavity = qtcavity.main:main']},
    zip_safe=False,
)
