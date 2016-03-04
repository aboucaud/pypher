===================
Convenience scripts
===================

addpixscl
=========

Write the pixel scale in FITS file headers

.. code:: bash

    $ addpixscl fits_files pixel_scale [--ext EXT]
    $ addpixscl (-h | --help)

Arguments
---------

``fits_files`` (*str* or list of *str*)
    name of FITS file(s)
``pixel_scale`` (*float*)
    pixel scale value in arcseconds


Options
-------

``-h, --help``
    print help
``-e, --ext`` (*int*)
    FITS extension number (default 0)

Examples
--------

This script works on single files

.. code:: bash
    
    $ addpixscl psf_a.fits 0.1

as well as on a list of files

.. code:: bash

    $ addpixscl psf*.fits 0.3 --ext 1
