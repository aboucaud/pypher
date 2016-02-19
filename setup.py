#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from setuptools import setup, find_packages

with open('make_psf_kernel.py') as fp:
    version_file = fp.read()
try:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    VERSION = version_match.group(1)
except AttributeError:
    VERSION = 'Unknown'


setup(
    name='make_psf_kernel',
    author='Alexandre Boucaud',
    author_email='alexandre.boucaud@ias.u-psud.fr',
    maintainer='Alexandre Boucaud',
    maintainer_email='boucaud.alexandre@gmail.com',
    description='Compute an homogenization kernel between two PSF',
    license='new BSD',
    url='https://git.ias.u-psud.fr/aboucaud/make_psf_kernel/',
    download_url='https://git.ias.u-psud.fr/aboucaud/make_psf_kernel/',
    version=VERSION,
    long_description=open('README.md').read(),
    zip_safe=False,
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mk-kernel = make_psf_kernel:main',
        ],
    },
    install_requires=[
        'numpy >= 1.6',
        'scipy >= 0.9',
        'pyfits >= 3.2'
    ],
    classifiers=[
      'Programming Language :: Python',
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: BSD License',
      'Intended Audience :: Science/Research',
      'Topic :: Scientific/Engineering :: Astronomy',
      'Operating System :: OS Independent',
      'Programming Language :: Python :: 2.7',
      'Programming Language :: Python :: 3.3+',
    ],
)
