#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import find_packages, setup
import os
import re


def read_files_in_path(path: str, pattern: str):
    return [file for file in os.listdir(path) if re.search(rf'{pattern}', file)]


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    author="Mitchell Lisle",
    description="Reflect App for Retros",
    install_requires=requirements,
    include_package_data=True,
    keywords='reflect',
    name='reflect',
    packages=find_packages('src'),
    package_data={
        'src.reflect.database.migrations': read_files_in_path('src/reflect/database/migrations', ".sql$"),
        'src.reflect.assets': read_files_in_path("src/reflect/assets", ".(png|jpeg|jpg|css)$")
    },
    package_dir={'': 'src'},
    url='https://github.com/mitchelllisle/reflect-app',
    version='0.1.0',
    zip_safe=False,
    entry_points={"console_scripts": ["reflect=reflect.main:main"]},
)
