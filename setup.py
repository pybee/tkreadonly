#/usr/bin/env python
from setuptools import setup

try:
    readme = open('README.rst')
    long_description = str(readme.read())
finally:
    readme.close()

setup(
    name='tkreadonly',
    version='0.6.0',
    description='A set of Tkinter widgets to display readonly text and code.',
    long_description=long_description,
    author='Russell Keith-Magee',
    author_email='russell@keith-magee.com',
    url='http://github.org/pybee/tkreadonly',
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
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
    test_suite='tests'
)
