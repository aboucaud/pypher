`make_psf_kernel`
================

Compute the homogenization kernel between two PSFs using Wiener filtering

#### Description

Quick summary of the tasks performed by this code:

  1. Replacing NaNs by zeros,
  2. Warping (rotation + resampling) of the PSFs (if necessary),
  3. Filtering in Fourier space using a regularized Wiener filter (details [here](method.md)),
  <!-- 4. Saving real and Fourier space versions of the produced kernel. -->
  4. Saving real space version of the produced kernel.

For simplicity, this code **does not** take care of:
  - the _interpolation_ of NaN values,
  - the _centering_ of the PSF images,
  - the _minimization_ of the kernel size.

#### Installation

There are two ways to get this code running:

  1. If you have `git` installed, the best way is to create a new directory and run the following command to retrieve the current version of the file,
    ```bash
    git clone git@git.ias.u-psud.fr:aboucaud/make_psf_kernel.git
    ```

  2. Otherwise you will find on top of the [main page](https://git.ias.u-psud.fr/aboucaud/make_psf_kernel) a download button to get a compressed archive containing the code.

To be able to run `make_psf_kernel`, you will need the following Python libraries installed: **numpy**, **scipy** and **pyfits (>= 3.3)**. If you have trouble installing these libraries, either contact the server administrator, or refer to [these instructions](https://git.ias.u-psud.fr/abeelen/python-notebook/blob/master/PythonInstall.md) for your personal computer.

Last, in order to run this code in any directory, you should add its location to your `PATH`.

#### Usage

```bash
make_psf_kernel <psf_input> <psf_target> <output>
                [--angle_input] [--angle_target] [-r, --reg_fact]
                [-v, --verbose] [-h, --help]
```

##### Args
- `psf_input`           path to the high resolution PSF (FITS image)
- `psf_target`          path to the low resolution PSF (FITS image)
- `output`              the output filename and path

##### Optionals
- `-h, --help`          print help (this)
- `-r, --reg_fact`      regularization factor [default `1.e-4`]
- `--angle_input`       rotation angle to apply to psf_input in deg [default `0`]
- `--angle_target`      rotation angle to apply to psf_target in deg [default `0`]
- `-v, --verbose`       print information while running the script

#### Example

An example bash script `run_herschel_bash.sh`, is provided along with this code (see [here](run_herschel_bash.sh)). Feel free to modify it to your needs.
Otherwise a short example of a call to the code is
```bash
make_psf_kernel psf_a.fits psf_b.fits kernel_a_to_b.fits -r 1.e-5
```
<!-- This will create two files in the current directory: `kernel_a_to_b.fits` and `kernel_a_to_b_dft.fits`. -->
This will create two files in the current directory: `kernel_a_to_b.fits` and `make_psf_kernel.log` where every useful information about the processing is stored.

#### Author
  Alexandre Boucaud <alexandre.boucaud@ias.u-psud.fr>

#### Version
  0.4
