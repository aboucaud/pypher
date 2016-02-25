#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 IAS / CNRS / Univ. Paris-Sud
# BSD License - see attached LICENSE file
# Author: Alexandre Boucaud <alexandre.boucaud@ias.u-psud.fr>

"""
fitsutils.py
------------

"""
from __future__ import absolute_import, print_function, division

try:
    import pyfits
except ImportError:
    import astropy.io.fits as pyfits

PIXSCL_KEY_DEG = ['CD1_1', 'CD1_2', 'CD2_1', 'CD2_2', 'CDELT1', 'CDELT2']
PIXSCL_KEY_ARCSEC = ['PIXSCALE', 'SECPIX', 'PIXSCALX', 'PIXSCALY']
PIXSCL_KEYS = PIXSCL_KEY_DEG + PIXSCL_KEY_ARCSEC


def has_pixelscale(fits_file):
    """Find pixel scale keywords in FITS file"""
    header = pyfits.getheader(fits_file)
    return [key
            for key in PIXSCL_KEYS
            if key in list(header.keys())]


def write_pixelscale(fits_file, value, ext=0):
    """
    Write pixel scale information to a FITS file header

    The input pixel scale value is given in arcseconds but is stored
    in degrees since the chosen header KEY is CDX_X

    Parameters
    ----------
    fits_file: str
        Path to a FITS image file
    value: float
        Pixel scale value in arcseconds
    ext: int, optional
        Extension number in the FITS file

    """
    pixscl = value / 3600
    comment = 'pixel scale in degrees'

    pyfits.setval(fits_file, 'CD1_1', value=pixscl, ext=ext, comment=comment)
    pyfits.setval(fits_file, 'CD1_2', value=0.0, ext=ext, comment=comment)
    pyfits.setval(fits_file, 'CD2_1', value=0.0, ext=ext, comment=comment)
    pyfits.setval(fits_file, 'CD2_2', value=pixscl, ext=ext, comment=comment)
