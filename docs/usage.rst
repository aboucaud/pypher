Getting Started
---------------

.. code:: bash

    $ pypher psf_source psf_target output
             [-s ANGLE_SOURCE] [-t ANGLE_TARGET] [-r REG_FACT]
    $ pypher (-h | --help)

Arguments
~~~~~~~~~

-  ``psf_source`` path to the high resolution PSF image (FITS file)
-  ``psf_target`` path to the low resolution PSF image (FITS file)
-  ``output`` the output filename and path

Options
~~~~~~~

-  ``-h, --help`` print help
-  ``-r, --reg_fact`` regularization factor (default 1.e-4)
-  ``-s, --angle_source`` rotation angle in deg to apply to
   ``psf_source`` (default 0)
-  ``-t, --angle_target`` rotation angle in deg to apply to
   ``psf_target`` (default 0)

Basic example
~~~~~~~~~~~~~

.. code:: bash

    $ pypher psf_a.fits psf_b.fits kernel_a_to_b.fits -r 1.e-5

This will create the desired kernel ``kernel_a_to_b.fits`` and a short
log ``kernel_a_to_b.log`` with information about the processing.

.. note::
  This can be disabled if needed
