#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='grocer',
      version='0.1.0',
      description='Things to do with groceries and data',
      url='http://github.com/ruizjme/grocer',
      author='Jaime Ruiz',
      author_email='jaimeruizno@gmail.com',
      license='MIT',
      packages=['grocer'],
      install_requires=['requests',],
      zip_safe=False
      )
