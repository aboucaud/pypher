# -*- coding: utf-8 -*-

# Copyright (c) 2016 IAS / CNRS / Univ. Paris-Sud
# BSD License - see attached LICENSE file
# Author: Alexandre Boucaud <alexandre.boucaud@ias.u-psud.fr>

from __future__ import division, absolute_import

import pytest
import numpy as np
import astropy.io.fits as fits

from numpy.testing import assert_equal, assert_allclose

from pypher.pypher import (parse_args, format_kernel_header,
                           imrotate, imresample, trim, zero_pad,
                           psf2otf, homogenization_kernel)
from pypher.fitsutils import has_pixelscale, get_pixscale, add_comments
from pypher.parser import ArgumentParserError
from pypher.addpixscl import parse_args as parse_args_addpixscl

ERRSHAPE = 'incorrect shape'
ERROUT = 'incorrect output'
ERRVAL = 'incorrect value'
PIXSCALE = 1.0
ABSTOL = 1e-6
RELTOL = 1e-6


class TestParser(object):
    def test_parse_args(self):
        with pytest.raises(ArgumentParserError):
            parse_args()

    def test_parse_args_addpixscl(self):
        with pytest.raises(ArgumentParserError):
            parse_args_addpixscl()


class TestFits(object):
    def test_nopixelscale(self, fitscleandir):
        with pytest.raises(IOError):
            get_pixscale('image.fits')

    def test_format_header(self, mock_parser):
        format_kernel_header('image.fits', mock_parser, PIXSCALE)
        assert round(fits.getval('image.fits', 'CD1_1') * 3600, 1) == PIXSCALE
        assert round(fits.getval('image.fits', 'CD1_2') * 3600, 1) == 0.0
        assert round(fits.getval('image.fits', 'CD2_1') * 3600, 1) == 0.0
        assert round(fits.getval('image.fits', 'CD2_2') * 3600, 1) == PIXSCALE

    def test_has_pixelscale(self):
        assert has_pixelscale('image.fits')

    def test_get_pixelscale(self):
        pscale = get_pixscale('image.fits')
        assert round(pscale, 1) == PIXSCALE

    def test_add_single_comment(self):
        add_comments('image.fits', "single comment")
        comments = str(fits.getval('image.fits', 'COMMENT')).split('\n')
        assert comments[-1] == "single comment"


class TestImageManipulation(object):
    def test_rotate90(self, imagerot):
        assert_allclose(imrotate(imagerot, 90), np.rot90(imagerot, 3),
                        atol=ABSTOL, rtol=RELTOL)

    def test_rotate180(self, imagerot):
        assert_allclose(imrotate(imagerot, 180), np.rot90(imagerot, 2),
                        atol=ABSTOL, rtol=RELTOL)

    def test_resample_even(self):
        size = 42
        factor = 2
        res = imresample(np.ones((size, size)),
                         source_pscale=factor,
                         target_pscale=1)
        assert res.shape[0] == size * factor

    def test_resample_odd(self):
        size = 49
        factor = 2
        res = imresample(np.ones((size, size)),
                         source_pscale=factor,
                         target_pscale=1)
        assert res.shape[0] == size * factor + 1

    def test_resample_memoryerror(self):
        with pytest.raises(MemoryError):
            imresample(np.zeros((200, 200)), 100, 1)

    def test_trim(self, tones):
        arr, size = tones
        size_e = size - 1
        size_o = size - 2
        shape_ee = (size_e, size_e)
        shape_eo = (size_e, size_o)
        shape_oo = (size_o, size_o)

        assert_equal(trim(arr, (size, size)), arr, ERROUT)
        # Shapes
        assert_equal(trim(arr, shape_oo).shape,
                     shape_oo,
                     ERRSHAPE)
        assert_equal(trim(arr, np.asarray(shape_oo, float)).shape,
                     shape_oo,
                     ERRSHAPE)
        # Wrong inputs
        with pytest.raises(ValueError):
            trim(arr, 0)
            trim(arr, (size_e, 0))
            trim(arr, (size + 1, size))
            trim(arr, shape_ee)
            trim(arr, shape_eo)

    def test_zero_pad(self, tones):
        arr, size = tones
        size_e = size + 1
        size_o = size + 2
        shape_ee = (size_e, size_e)
        shape_eo = (size_e, size_o)
        shape_oo = (size_o, size_o)

        assert_equal(zero_pad(arr, (size, size)), arr, ERROUT)
        # Shapes
        for pos in ['corner', 'center']:
            assert_equal(zero_pad(arr, shape_ee, 'corner').shape,
                         shape_ee,
                         ERRSHAPE)
            assert_equal(zero_pad(arr, shape_oo, pos).shape,
                         shape_oo,
                         ERRSHAPE)
            assert_equal(zero_pad(arr, shape_eo, 'corner').shape,
                         shape_eo,
                         ERRSHAPE)
            # Wrong inputs
            with pytest.raises(ValueError):
                zero_pad(arr, -2, position=pos)
                zero_pad(arr, size_e, position=pos)
                zero_pad(arr, (size - 1, size_e), pos)
                zero_pad(arr, shape_ee, 'center')
                zero_pad(arr, shape_eo, 'center')


class TestFourier(object):
    def test_dirac_otf(self, imagedirac):
        shape = imagedirac.shape
        assert_equal(psf2otf(imagedirac, shape), np.ones(shape))

    def test_homogenization_dtype(self, imagedirac):
        center = imagedirac.shape[0] // 2
        target = np.zeros_like(imagedirac)
        s = slice(center - 1, center + 2)
        target[s, s] += 1.
        target[center, center] += 1
        target /= target.sum()

        k, kf = homogenization_kernel(target, imagedirac,
                                      reg_fact=1e-4, clip=True)

        assert k.dtype == float
        assert kf.dtype == complex
