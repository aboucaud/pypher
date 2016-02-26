

***************************************
PSF Homogenization kERnels - ``pypher``
***************************************

Compute the homogenization kernel between two PSFs

Features:

1. Replace NaNs by zeros,
2. Warps (rotation + resampling) the PSFs if necessary,
3. Filtering in Fourier space using a regularized Wiener filter (details
   `here <method.md>`__),
4. Saving real space version of the produced kernel.

.. note::
    ``pypher`` needs the pixel scale information to be present in the FITS files.
    If not, use the provided ``addpixscl`` method to add this missing info.

For simplicity, this code **does not** take care of: - the
*interpolation* of NaN values, - the *centering* of the PSF images, -
the *minimization* of the kernel size.


Quick install
=============

To install pypher, simply:

.. code:: bash

    $ pip install pypher

and start working with it right away:

.. code:: bash

    $ pypher psf_a.fits psf_b.fits kernel_a_to_b.fits

Other installation procedures are described in :ref:`installation`.

User Guide:
==========

.. toctree::
   :maxdepth: 2

   installation
   usage
   convenience
   contribution


Acknowledging
=============

If you make use of any product of this code in a scientific publication,
please consider acknowledging the work by citing the following paper

Boucaud, Bocchio *et al.* (2015) *in prep.*

.. Licence
.. =======

.. This work is licensed under a 3-clause BSD style license - see `license`_.


:Authors:
    Alexandre Boucaud <alexandre.boucaud@ias.u-psud.fr>

:Licence:
    This work is licensed under a 3-clause BSD style license - see license_.

.. _license: https://git.ias.u-psud.fr/aboucaud/pypher/blob/packaging/LICENSE
