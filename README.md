`pypher` - Python-based PSF Homogenization kERnels
==================================================

Compute the homogenization kernel between two PSFs

Features
--------

  1. Replacing NaNs by zeros,
  2. Warping (rotation + resampling) of the PSFs (if necessary),
  3. Filtering in Fourier space using a regularized Wiener filter,
  4. Producing an image space homogenization kernel.

This code **does not** take care of:
  - the _interpolation_ of NaN values,
  - the _centering_ of the PSF images,
  - the _minimization_ of the kernel size.

Installation
------------
PyPHER works both with Python 2.7 and 3.3 or later

### Option 1: [Pip](https://pypi.python.org/pypi/pypher)

```bash
$ pip install pypher
```

### Option 2: from source

```bash
$ git clone https://git.ias.u-psud.fr/aboucaud/pypher.git
$ cd pypher
$ python setup.py install
```

#### Dependencies

As listed in the [requirements.txt](requirements.txt), the following Python libraries need to be installed:
- [numpy](http://www.numpy.org/) (>=1.7.2)
- [scipy](http://www.scipy.org/) (>=0.9.0)
- [pyfits](http://www.stsci.edu/institute/software_hardware/pyfits/) (>= 3.2) or [astropy](http://www.astropy.org/) (>=1.0.8)

In case these are not automatically installed during the above procedures, simply use:
```bash
$ pip install -r requirements.txt
```


Usage
-----

```bash
$ pypher psf_source psf_target output
         [-s ANGLE_SOURCE] [-t ANGLE_TARGET] [-r REG_FACT]
$ pypher (-h | --help)
```

### Arguments
- `psf_source`          path to the high resolution PSF image (FITS file)
- `psf_target`          path to the low resolution PSF image (FITS file)
- `output`              the output filename and path

### Options
- `-h, --help`          print help
- `-r, --reg_fact`      regularization factor (default 1.e-4)
- `-s, --angle_source`  rotation angle in deg to apply to `psf_source` (default 0)
- `-t, --angle_target`  rotation angle in deg to apply to `psf_target` (default 0)

### Basic example

```bash
$ pypher psf_a.fits psf_b.fits kernel_a_to_b.fits -r 1.e-5
```

This will create the desired kernel `kernel_a_to_b.fits` and a short log `kernel_a_to_b.log` with information about the processing.


Acknowledging
-------------

If you make use of any product of this code in a scientific publication, please consider acknowledging the work by citing the following paper

Boucaud, Bocchio _et al._ (2016) _in prep._

Contributing
------------

We welcome all contributions.

To report any bugs or file feature requests, please use the [issue tracker](https://git.ias.u-psud.fr/aboucaud/pypher/issues).
Otherwise feel free to fork the repository, make your own changes and send a pull request.


Licence
-------
This work is licensed under a 3-clause BSD style license - see [LICENSE](LICENSE) file.
