#/usr/bin/env python
import sys

from setuptools import setup
from tkreadonly import VERSION

try:
    readme = open('README.rst')
    long_description = str(readme.read())
finally:
    readme.close()

setup(
    name='tkreadonly',
    version=VERSION,
    description='A set of Tkinter widgets to display readonly text and code.',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    url='http://github.org/tkreadonly',
    py_modules=[
        'tkreadonly',
    ],
    install_requires=[
        'Pygments>=1.5'
    ],
    scripts=[],
    license='New BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    test_suite='tests'
)