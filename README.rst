====================================================
PyPHER - Python-based PSF Homogenization kERnels
====================================================

Compute an homogenization kernel between two PSFs.

This code is well suited for PSF matching applications in both an astronomical or microscopy context.

It has been developed as part of the ESA `Euclid <http://www.cosmos.esa.int/web/euclid>`_ mission and is currently being used for multi-band photometric studies of `HST <https://www.spacetelescope.org/>`_ (visible) and `Herschel <http://www.cosmos.esa.int/web/herschel/home>`_ (IR) data.


Features
========

1. **Warp** (rotation + resampling) the PSF images (if necessary),
2. **Filter** images in Fourier space using a regularized Wiener filter,
3. **Produce** a homogenization kernel.

**Note:** ``pypher`` needs the pixel scale information to be present in the FITS files. If not, use the provided ``addpixscl`` method to add this missing info.

**Warning:** This code **does not**    

    * interpolate NaN values (replaced by 0 instead),
    * center PSF images,
    * minimize the kernel size.


Installation
============

PyPHER works both with Python 2.7 and 3.3 or later and relies on `numpy <http://www.numpy.org/>`_, `scipy <http://www.scipy.org/>`_ and `pyfits <http://www.stsci.edu/institute/software_hardware/pyfits/>`_ (or `astropy <http://www.astropy.org/>`_) libraries.

Option 1: `Pip <https://pypi.python.org/pypi/pypher>`_
------------------------------------------------------

.. code:: bash

    $ pip install pypher

Option 2: from `source <https://git.ias.u-psud.fr/aboucaud/pypher>`_
--------------------------------------------------------------------

.. code:: bash

    $ git clone https://git.ias.u-psud.fr/aboucaud/pypher.git
    $ cd pypher
    $ python setup.py install


Basic example
=============

.. code:: bash

    $ pypher psf_a.fits psf_b.fits kernel_a_to_b.fits -r 1.e-5

This will create the desired kernel ``kernel_a_to_b.fits`` and a short
log ``kernel_a_to_b.log`` with information about the processing.


Acknowledging
=============

If you make use of any product of this code in a scientific publication,
please consider acknowledging the work by citing the following paper

Boucaud, Bocchio *et al.* (2016) *in prep.*

**Note:** To be submitted **soon**