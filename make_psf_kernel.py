#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 IAS / CNRS / Univ. Paris-Sud
# New BSD License
# Author: Alexandre Boucaud <alexandre.boucaud@ias.u-psud.fr>

"""
===============
make_psf_kernel
===============
Compute the homogenization kernel between two PSFs

Usage:
  make_psf_kernel <psf_source> <psf_target> <output>
                  [--angle_source] [--angle_target] [-r, --reg_fact]
                  [-h, --help]

Args:
  psf_source          path to the high resolution PSF (FITS image)
  psf_target          path to the low resolution PSF (FITS image)
  output              the output filename and path

Optionals:
  -h, --help          print help (this)
  -r, --reg_fact      regularization factor [default 1.e-4]
  --angle_source      rotation angle to apply to psf_source in deg
                      [default 0]
  --angle_target      rotation angle to apply to psf_target in deg
                      [default 0]

Example:
  make_psf_kernel psf_a.fits psf_b.fits kernel_a_to_b.fits -r 1.e-5

Author:
  Alexandre Boucaud <alexandre.boucaud@ias.u-psud.fr>

Version:
  0.5

"""
from __future__ import print_function, division

import os
import sys
import numpy as np
import numpy.random as npr
import logging
try:
    import astropy.io.fits as pyfits
except ImportError:
    import pyfits
from os import path
from scipy.ndimage import rotate, zoom
from logging.handlers import RotatingFileHandler

__version__ = '0.5'


def parse_args():
    import argparse
    # Starts with command line parsing
    parser = argparse.ArgumentParser(
        description="Compute the homogenization kernel between two PSFs")

    parser.add_argument(
        'psf_input',
        nargs='?',
        metavar='psf_input',
        type=str,
        help="the kernel with highest resolution")

    parser.add_argument(
        'psf_target',
        nargs='?',
        metavar='psf_target',
        type=str,
        help="the kernel with lowest resolution")

    parser.add_argument(
        'output',
        nargs='?',
        metavar='output',
        type=str,
        help="output file name")

    parser.add_argument(
        '--angle_input',
        nargs='?',
        metavar='angle_input',
        type=float,
        default=0.0,
        const=0.0,
        dest='angle_input',
        help="rotation angle in degrees to apply to `psf_input`")

    parser.add_argument(
        '--angle_target',
        nargs='?',
        metavar='angle_target',
        type=float,
        default=0.0,
        const=0.0,
        dest='angle_target',
        help="rotation angle in degrees to apply to `psf_target`")

    parser.add_argument(
        '-r',
        '--reg_fact',
        nargs='?',
        metavar='reg_fact',
        type=float,
        default=1.e-4,
        const=1.e-4,
        dest='reg_fact',
        help="regularisation parameter for the Wiener filter")

    return parser.parse_args()

################
# IMAGE METHODS
################


def get_pixscale(filename):
    """Retreive the image pixel scale in its FITS header"""
    header = pyfits.getheader(filename)
    pixel_key = ''
    pkey_list = ['PIXSCALE', 'PIXSCALX', 'SECPIX',
                 'CDELT1', 'CDELT2', 'CD1_1']
    for key in pkey_list:
        if key in header.keys():
            pixel_key = key
            break
    if not pixel_key:
        raise IOError("Pixel size not found in FITS file")

    pixel_scale = abs(header[pixel_key])
    if pixel_key in ['CDELT1', 'CDELT2', 'CD1_1']:
        pixel_scale *= 3600

    return pixel_scale


def format_kernel_header(fits, args, pixel_scale):
    """
    Format the output kernel header

    Parameters
    ----------
    args: Argument Parser

    Returns
    -------
    header: `pyfits.Header`
        Output kernel formatted header

    """
    hdr = fits.header
    for comment_key in ['COMMENT', 'comment', 'Comment']:
        if comment_key in hdr.keys():
            del hdr[comment_key]
    hdr.add_comment('='*50)
    hdr.add_comment('')
    hdr.add_comment('File written with make_psf_kernel')
    hdr.add_comment('')
    hdr.add_comment('Kernel from PSF')
    hdr.add_comment('=> {}'.format(path.basename(args.psf_source)))
    hdr.add_comment('to PSF')
    hdr.add_comment('=> {}'.format(path.basename(args.psf_target)))
    hdr.add_comment('using a regularisation parameter '
                    'R = {:1.1e}'.format(args.reg_fact))
    hdr.add_comment('')
    hdr.add_comment('='*50)

    for psc_key in ['PIXSCALE', 'PIXSCALX', 'SECPIX',
                    'CDELT1', 'CDELT2', 'CD1_1']:
        if psc_key in hdr.keys():
            del hdr[psc_key]
    hdr['CD1_1'] = (pixel_scale, "pixel scale in deg.")
    hdr['CD1_2'] = (0, "pixel scale in deg.")
    hdr['CD2_1'] = (0, "pixel scale in deg.")
    hdr['CD2_2'] = (pixel_scale, "pixel scale in deg.")


def imrotate(image, angle, interp_order=1):
    """Rotate an image from North to East given an angle in degrees

    Parameters
    ----------
    image : `numpy.ndarray`
        Input data array
    angle : float
        Angle in degrees
    interp_order : int, optional
        Spline interpolation order [0, 5] (default 1: linear)

    Returns
    -------
    output : `numpy.ndarray`
        Rotated data array

    """
    return rotate(image, -1.0 * angle,
                  order=interp_order, reshape=False, prefilter=False)


def imresample(image, source_pscale, target_pscale, interp_order=1):
    """Resample data array from one pixel scale to another

    Parameters
    ----------
    image : `numpy.ndarray`
        Input data array
    source_pscale : float
        Pixel scale of ``image`` in arcseconds
    target_pscale : float
        Pixel scale of output array in arcseconds
    interp_order : int, optional
        Spline interpolation order [0, 5] (default 1: linear)

    Returns
    -------
    output : `numpy.ndarray`
        Resampled data array

    """
    old_size = image.shape[0]
    new_size_raw = old_size * source_pscale / target_pscale
    new_size = int(round(new_size_raw))
    ratio = new_size / old_size
    if new_size > 10000:
        raise MemoryError()

    return zoom(image, ratio, order=interp_order) / ratio**2


def trim(image, shape):
    """Trim image to a given shape

    Parameters
    ----------
    image: 2D `numpy.ndarray`
        Input image
    shape: tuple of int
        Desired output shape of the image

    Returns
    -------
    new_image: 2D `numpy.ndarray`
        Input image trimmed

    """
    shape = np.asarray(shape, dtype=int)
    imshape = np.asarray(image.shape, dtype=int)

    if np.alltrue(imshape == shape):
        return image

    if np.any(shape <= 0):
        raise ValueError("TRIM: null or negative shape given")

    dshape = imshape - shape
    if np.any(dshape < 0):
        raise ValueError("TRIM: target size bigger than source one")

    if np.any(dshape % 2 != 0):
        raise ValueError("TRIM: source and target shapes have different parity")

    idx, idy = np.indices(shape)
    offx, offy = dshape // 2

    return image[idx + offx, idy + offy]


def zero_pad(image, shape, position='corner'):
    """
    Extends image to a certain size with zeros

    Parameters
    ----------
    image: real 2d `numpy.ndarray`
        Input image
    shape: tuple of int
        Desired output shape of the image
    position : str, optional
        The position of the input image in the output one:
            * 'corner'
                top-left corner (default)
            * 'center'
                centered

    Returns
    -------
    padded_img: real `numpy.ndarray`
        The zero-padded image

    """
    shape = np.asarray(shape, dtype=int)
    imshape = np.asarray(image.shape, dtype=int)

    if np.alltrue(imshape == shape):
        return image

    if np.any(shape <= 0):
        raise ValueError("ZERO_PAD: null or negative shape given")

    dshape = shape - imshape
    if np.any(dshape < 0):
        raise ValueError("ZERO_PAD: target size smaller than source one")

    pad_img = np.zeros(shape, dtype=image.dtype)

    idx, idy = np.indices(imshape)

    if position == 'center':
        if np.any(dshape % 2 != 0):
            raise ValueError("ZERO_PAD: source and target shapes "
                             "have different parity.")
        offx, offy = dshape // 2
    else:
        offx, offy = (0, 0)

    pad_img[idx + offx, idy + offy] = image

    return pad_img


##########
# FOURIER
##########


def udft2(image):
    """Unitary fft2"""
    norm = np.sqrt(image.size)
    return np.fft.fft2(image) / norm


def uidft2(image):
    """Unitary ifft2"""
    norm = np.sqrt(image.size)
    return np.fft.ifft2(image) * norm


def psf2otf(psf, shape):
    """
    Convert point-spread function to optical transfer function.

    Compute the Fast Fourier Transform (FFT) of the point-spread
    function (PSF) array and creates the optical transfer function (OTF)
    array that is not influenced by the PSF off-centering.
    By default, the OTF array is the same size as the PSF array.

    To ensure that the OTF is not altered due to PSF off-centering, PSF2OTF
    post-pads the PSF array (down or to the right) with zeros to match
    dimensions specified in OUTSIZE, then circularly shifts the values of
    the PSF array up (or to the left) until the central pixel reaches (1,1)
    position.

    Parameters
    ----------
    psf : `numpy.ndarray`
        PSF array
    shape : int
        Output shape of the OTF array

    Returns
    -------
    otf : `numpy.ndarray`
        OTF array

    Notes
    -----
    Adapted from MATLAB psf2otf function

    """
    if np.all(psf == 0):
        otf = np.zeros_like(psf)
    else:
        inshape = psf.shape
        # Pad the PSF to outsize
        psf = zero_pad(psf, shape, position='corner')

        # Circularly shift OTF so that the 'center' of the PSF is
        # [0,0] element of the array
        for axis, axis_size in enumerate(inshape):
            psf = np.roll(psf, -int(axis_size / 2), axis=axis)

        # Compute the OTF
        otf = np.fft.fft2(psf)

        # Estimate the rough number of operations involved in the FFT
        # and discard the PSF imaginary part if within roundoff error
        # roundoff error  = machine epsilon = sys.float_info.epsilon
        # or np.finfo().eps
        n_ops = np.sum(psf.size * np.log2(psf.shape))
        otf = np.real_if_close(otf, tol=n_ops)

    return otf


################
# DECONVOLUTION
################

LAPLACIAN = np.array([[ 0, -1,  0],
                      [-1,  4, -1],
                      [ 0, -1,  0]])


def deconv_wiener(psf, reg_fact):
    """Create a Wiener filter using a PSF image

    The signal is $\ell_2$ penalized by a 2D Laplacian operator that
    serves as a high-pass filter for the regularization process.
    The key to the process is to use optical transfer functions (OTF)
    instead of simple Fourier transform, since it ensures the phase
    of the psf is adequately placed.

    Parameters
    ----------
    psf: `numpy.ndarray`
        PSF array
    reg_fact: float
        Regularisation parameter for the Wiener filter

    Returns
    -------
    wiener: complex `numpy.ndarray`
        Fourier space Wiener filter

    """
    # Optical transfer functions
    trans_func = psf2otf(psf, psf.shape)
    reg_op = psf2otf(LAPLACIAN, psf.shape)

    wiener = np.conj(trans_func) / (np.abs(trans_func)**2 +
                                    reg_fact * np.abs(reg_op)**2)

    return wiener


def homogenization_kernel(psf_target, psf_source, reg_fact=1e-4, clip=True):
    """
    Compute the homogenization kernel to match two PSFs

    The deconvolution step is done using a Wiener filter with $\ell_2$
    penalization.
    The output is given both in Fourier and in the image domain to serve
    different purposes.

    Parameters
    ----------
    psf_target: `numpy.ndarray`
        2D array
    psf_source: `numpy.ndarray`
        2D array
    reg_fact: float, optional
        Regularisation parameter for the Wiener filter
    clip: bool, optional
        If `True`, enforces the non-amplification of the noise
        (default `True`)

    Returns
    -------
    kernel_image: `numpy.ndarray`
        2D deconvolved image
    kernel_fourier: `numpy.ndarray`
        2D discrete Fourier transform of deconvolved image

    """
    wiener = deconv_wiener(psf_source, reg_fact)

    kernel_fourier = wiener * udft2(psf_target)
    kernel_image = np.real(uidft2(kernel_fourier))

    if clip:
        kernel_image.clip(-1, 1)

    return kernel_image, kernel_fourier


def deconv_unsup_wiener(data, source, clip=True, user_settings=None):
    """Return an estimation of the regularisation parameter

    Return an estimation of the regularisation parameter by
    unsupervised Wiener-Hunt deconvolution, see References.

    Parameters
    ----------
    data: `numpy.ndarray`
        2D image of data to process
    source: `numpy.ndarray`
        2D source PSF image
    clip: bool, optional
        If `True`, enforces the non-amplification of the noise
        (default `True`)
    user_settings: dict, optional
        settings of the algorithm, see source.

    Returns
    -------
    reg_val: float
        an estimation of  the regularisation parameter need for the data set.
    extra: dict
        additionnal products of the algorithm, see source.

    References
    ----------
    .. [1] François Orieux, Jean-François Giovannelli, and Thomas
           Rodet, "Bayesian estimation of regularization and point
           spread function parameters for Wiener-Hunt deconvolution",
           J. Opt. Soc. Am. A 27, 1593-1607 (2010)

    http://www.opticsinfobase.org/josaa/abstract.cfm?URI=josaa-27-7-1593
    """
    settings = {'threshold': 1e-4, 'max_iter': 200,
                'min_iter': 100, 'burnin': 30}
    settings = settings.update(user_settings) if user_settings else settings

    # Optical transfer function for the source PSF
    trans_func = psf2otf(source, source.shape)
    # for the regularization operator (high pass here)
    reg_op = psf2otf(LAPLACIAN, source.shape)

    # The mean of the object
    x_postmean = np.zeros(trans_func.shape)
    # The previous computed mean in the iterative loop
    prev_x_postmean = np.zeros(trans_func.shape)

    # Difference between two successive mean
    delta = np.NAN

    # Initial state of the chain
    gn_chain, gx_chain = [1], [1]

    # The correlation of the object in Fourier space (if size is big,
    # this can reduce computation time in the loop)
    areg2 = np.abs(reg_op)**2
    atf2 = np.abs(trans_func)**2

    data_size = data.size
    data = udft2(data)

    # Gibbs sampling
    for iteration in range(settings['max_iter']):
        # Sample of Eq. 27 p(circX^k | gn^k-1, gx^k-1, y).

        # weighing (correlation in direct space)
        precision = gn_chain[-1] * atf2 + gx_chain[-1] * areg2  # Eq. 29
        excursion = npr.standard_normal(data.shape) / np.sqrt(precision)

        # mean Eq. 30 (RLS for fixed gn, gamma0 and gamma1 ...)
        wiener_filter = gn_chain[-1] * np.conj(trans_func) / precision
        x_mean = wiener_filter * data

        # sample of X in Fourier space
        x_sample = x_mean + excursion

        # sample of Eq. 31 p(gn | x^k, gx^k, y)
        likelihood = np.sum(np.abs(data - x_sample * trans_func)**2)
        gn_chain.append(npr.gamma(data_size / 2, 2 / likelihood))

        # sample of Eq. 31 p(gx | x^k, gn^k-1, y)
        smoothness = np.sum(np.abs(x_sample * reg_op)**2)
        gx_chain.append(npr.gamma((data_size - 1) / 2, 2 / smoothness))

        # current empirical average
        if iteration > settings['burnin']:
            x_postmean = prev_x_postmean + x_sample

        if iteration > (settings['burnin'] + 1):
            norm = np.sum(np.abs(x_postmean)) / (iteration -
                                                 settings['burnin'])
            current = x_postmean / (iteration - settings['burnin'])
            previous = prev_x_postmean / (iteration - settings['burnin'] - 1)

            delta = np.sum(np.abs(current - previous)) / norm

        prev_x_postmean = x_postmean

        # stop of the algorithm
        if (iteration > settings['min_iter']) and \
           (delta < settings['threshold']):
            break

    # Empirical average \approx POSTMEAN Eq. 44
    x_postmean = x_postmean / (iteration - settings['burnin'])
    x_postmean = np.real(uidft2(x_postmean))

    if clip:
        x_postmean.clip(-1, 1)

    return (np.mean(gx_chain[settings['burnin']:]) /
            np.mean(gn_chain[settings['burnin']:]),
            {'image': x_postmean,
             'noise': np.mean(gn_chain[settings['burnin']:]),
             'prior': np.mean(gn_chain[settings['burnin']:]),
             'noise_uncertainty': np.std(gn_chain[settings['burnin']:]),
             'prior_uncertainty': np.std(gn_chain[settings['burnin']:]),
             'regul_uncertainty': np.std(gn_chain[settings['burnin']:]) /
             np.std(gn_chain[settings['burnin']:])})


########
# DEBUG
########


def setup_logger(log_filename='make_psf_kernel.log'):
    """Sets up a logger"""
    # create logger
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    # Add the log message handler to the logger
    handler = RotatingFileHandler(log_filename)
    # create formatter
    formatter = logging.Formatter('%(asctime)s - '
                                  '%(module)s - '
                                  '%(levelname)s - '
                                  '%(message)s')
    handler.setFormatter(formatter)
    # add handler to logger
    logger.addHandler(handler)

    return logger


#######
# MAIN
#######


def main():
    args = parse_args()

    logname = 'make_psf_kernel.log'
    if os.path.exists(logname):
        os.remove(logname)
    log = setup_logger(logname)

    # Load images (NaNs are set to 0)
    psf_source = pyfits.getdata(args.psf_source)
    psf_target = pyfits.getdata(args.psf_target)

    log.info('Source PSF loaded: %s' % args.psf_source)
    log.info('Target PSF loaded: %s' % args.psf_target)

    # Set NaNs to 0.0
    psf_source = np.nan_to_num(psf_source)
    psf_target = np.nan_to_num(psf_target)

    # Retrieve the pixel scale of each image
    pixscale_source = get_pixscale(args.psf_source)
    pixscale_target = get_pixscale(args.psf_target)

    log.info('Source PSF pixel scale: %.2f arcsec' % pixscale_source)
    log.info('Target PSF pixel scale: %.2f arcsec' % pixscale_target)

    # Rotate images (if necessary)
    if args.angle_source != 0.0:
        psf_source = imrotate(psf_source, args.angle_source)
    if args.angle_target != 0.0:
        psf_target = imrotate(psf_target, args.angle_target)

    log.info('Source PSF rotated by %.2f degrees' % args.angle_source)
    log.info('Target PSF rotated by %.2f degrees' % args.angle_target)

    # Normalize the PSFs
    psf_source /= psf_source.sum()
    psf_target /= psf_target.sum()

    # Resample high resolution image to the low one
    if pixscale_source != pixscale_target:
        try:
            psf_source = imresample(psf_source, pixscale_source, pixscale_target)
        except MemoryError:
            log.error('- COMPUTATION ABORTED -')
            log.error('The size of the resampled PSF would have '
                      'exceeded 10K x 10K')
            log.error('Please resize your image and try again')

            print('Issue during the resampling step - see make_psf_kernel.log')
            sys.exit()

        log.info('Source PSF resampled to the target pixel scale')

    # check the new size of the source vs. the target
    if ((psf_source.shape[0] > psf_target.shape[0]) or
        (psf_source.shape[1] > psf_target.shape[1])):
        psf_source = trim(psf_source, psf_target.shape)
    else:
        psf_source = zero_pad(psf_source, psf_target.shape, position='center')

    kernel, kernel_fourier = homogenization_kernel(psf_target, psf_source,
                                                   reg_fact=args.reg_fact)

    log.info('Kernel computed using Wiener filtering and a regularisation '
             'parameter r = %.2e' % args.reg_fact)

    # Write kernel to FITS file
    kernel_hdu = pyfits.PrimaryHDU(data=kernel)
    format_kernel_header(kernel_hdu, args, pixscale_target)
    kernel_hdu.writeto(args.output)
    # Write Fourier space kernel to FITS file
    # print("Currently the code does not save the Fourier transform "
    #       "in a FITS file")
    # outbase, outext = path.splitext(outfile)
    # outfile_dft = path.join(outbase, "_dft", outext)
    # tkfits_fourier = pyfits.PrimaryHDU(data=tk_fourier)
    # format_kernel_header(tkfits_fourier, args, pixscale_target)
    # tkfits_fourier.writeto(outfile_dft)

    log.info('Kernel saved in {0.output}'.format(args))

    print("make_psf_kernel: Output kernels saved in {0.output}".format(args))


if __name__ == '__main__':
    try:
        main()
    except:
        print(__doc__)
        raise
