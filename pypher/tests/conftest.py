# -*- coding: utf-8 -*-

# Copyright (c) 2016 IAS / CNRS / Univ. Paris-Sud
# BSD License - see attached LICENSE file
# Author: Alexandre Boucaud <alexandre.boucaud@ias.u-psud.fr>

from __future__ import division

import os
import tempfile
import collections

import pytest
import numpy as np
import astropy.io.fits as fits


def create_mock_fits():
    x = np.ones((5, 5))
    prihdu = fits.PrimaryHDU(x)

    # Single extension FITS
    img = fits.ImageHDU(data=x)
    singlehdu = fits.HDUList([prihdu, img])
    singlehdu.writeto('image.fits', overwrite=True)


@pytest.fixture(scope="module")
def fitscleandir():
    newpath = tempfile.mkdtemp()
    os.chdir(newpath)
    create_mock_fits()


@pytest.fixture
def mock_parser():
    MockParser = collections.namedtuple('MockParser',
                                        ['psf_source', 'psf_target', 'output',
                                         'angle_source', 'angle_target',
                                         'reg_fact'])
    parser = MockParser(psf_source='psf_source.fits',
                        psf_target='psf_target.fits',
                        output='output.fits',
                        angle_source=0.0,
                        angle_target=0.0,
                        reg_fact=1.e-4)
    return parser


@pytest.fixture(scope='function', params=[15, 55, 255])
def tones(request):
    size = request.param
    return np.ones((size, size)), size


@pytest.fixture(scope='function', params=[0.11, 0.22, 0.33])
def trange(request):
    step = request.param
    return np.arange(0, 10, step)


@pytest.fixture(scope='function', params=[5, 10])
def floatrange(request):
    return request.param


@pytest.fixture(scope='function', params=[3, 15, 101])
def imagerot(request):
    size = request.param
    array = np.zeros((size, size))
    array[0, size//2] = 1
    return array


@pytest.fixture(scope='function', params=[3, 15, 100])
def imagedirac(request):
    size = request.param
    array = np.zeros((size, size))
    array[size // 2, size // 2] = 1
    return array
