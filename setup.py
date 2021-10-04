#!/usr/bin/env python3
from distutils.core import setup

ext_modules = []
cmdclass = {}

setup(
    name='tabulatorz',
    version='0.0.0',
    description='',
    url='http://github.com/ishmaelbelghazi/uimnet',
    author='David Lopez-Paz and Mohamed Ishmael Belghaz',
    author_email='ishmael.belghazi@gmail.com',
    license='MIT',
    packages=['tabulatorz'],
    cmdclass=cmdclass,
    ext_modules=ext_modules,
)
