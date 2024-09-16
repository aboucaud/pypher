====================================================
PyPHER - Python-based PSF Homogenization kERnels
====================================================

|pypi| |docs| |license| |doi| |actions|

Compute an homogenization kernel between two PSFs.

This code is well suited for PSF matching applications in both an astronomical or microscopy context.

It has been developed as part of the ESA `Euclid <http://www.cosmos.esa.int/web/euclid>`_ mission and is currently being used for multi-band photometric studies of `HST <https://www.spacetelescope.org/>`_ (visible) and `Herschel <http://www.cosmos.esa.int/web/herschel/home>`_ (IR) data.

:Paper: http://arxiv.org/abs/1609.02006
:Documentation: https://pypher.readthedocs.io

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

PyPHER works both with Python 2.7 and 3.X and relies on `numpy <http://www.numpy.org/>`_, `scipy <http://www.scipy.org/>`_ and `astropy <http://www.astropy.org/>`_ libraries.

Option 1: `Pip <https://pypi.python.org/pypi/pypher>`_
------------------------------------------------------

.. code:: bash

    pip install pypher

Option 2: from `source <https://github.com/aboucaud/pypher>`_
-------------------------------------------------------------

.. code:: bash

    git clone https://github.com/aboucaud/pypher
    cd pypher
    python setup.py install

Option 3: from `conda-forge <https://github.com/conda-forge/pypher-feedstock>`_
-------------------------------------------------------------------------------

.. code:: bash

    conda install -c conda-forge pypher

Basic example
=============

.. code:: bash

    $ pypher psf_a.fits psf_b.fits kernel_a_to_b.fits -r 1.e-5

This will create the desired kernel ``kernel_a_to_b.fits`` and a short
log ``kernel_a_to_b.log`` with information about the processing.


Acknowledging
=============

If you make use of any product of this code in a scientific publication,
please consider acknowledging the work by citing the paper using the BibTeX 
information in the ``Cite this repository`` section at the top right of the page.


.. |pypi| image:: https://img.shields.io/pypi/v/pypher.svg
    :alt: Latest Version
    :scale: 100%
    :target: https://pypi.python.org/pypi/pypher

.. |docs| image:: https://readthedocs.org/projects/pypher/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://pypher.readthedocs.org/en/latest/?badge=latest

.. |actions| image:: https://github.com/aboucaud/pypher/actions/workflows/pytest.yml/badge.svg
    :alt: GitHub CI
    :scale: 100%
    :target: https://github.com/aboucaud/pypher/actions/workflows/pytest.yml

.. |license| image:: https://img.shields.io/badge/license-BSD-blue.svg?style=flat
    :alt: License type
    :scale: 100%
    :target: https://github.com/aboucaud/pypher/blob/master/LICENSE

.. |doi| image:: https://zenodo.org/badge/21241/aboucaud/pypher.svg
    :alt: DOI number
    :scale: 100%
    :target: https://zenodo.org/badge/latestdoi/21241/aboucaud/pypher

.. |arxiv| image:: http://img.shields.io/badge/arXiv-1609.02006-yellow.svg?style=flat
     :alt: arXiv paper
     :scale: 100%
     :target: https://arxiv.org/abs/1609.02006

