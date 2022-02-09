#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['requests', ]

setup_requirements = ['pytest-runner', 'setuptools', 'wheel', 'bumpversion']

test_requirements = ['pytest', 'coverage', ]

setup(
    author="Júlio Vaz",
    author_email='jvaz@stone.com.br',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Simple python authorization library.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='python_authorization',
    name='python_authorization',
    # packages=find_packages(include=['pyglobal_identity']),
    packages=find_packages(exclude=['tests']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/julio-vaz/python-authorization',
    version='1.0.4',
    zip_safe=False,
)
