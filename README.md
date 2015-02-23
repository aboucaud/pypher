`make_psf_kernel`
================
Compute the homogenization kernel between two PSFs using Wiener filtering

#### Usage

```bash
make_psf_kernel <psf_input> <psf_target> <output>
                [-r, --reg_fact] [-f, --fourier]
                [--angle_input] [--angle_target]
                [-v, --verbose]
                [-h, --help]
```

#### Args
- `psf_input`           path to the high resolution PSF (FITS image)
- `psf_target`          path to the low resolution PSF (FITS image)
- `output`              the output filename and path

#### Optionals
- `-h, --help`          print help (this)
- `-r, --reg_fact`      regularization factor [default `1.e-4`]
- `-f, --fourier`       return the Fourier space version of the kernel
- `--angle_input`       rotation angle to apply to psf_input in deg [default `0`]
- `--angle_target`      rotation angle to apply to psf_target in deg [default `0`]
- `-v, --verbose`       print information while running the script

#### Example

```bash
make_psf_kernel psf_a.fits psf_b.fits kernel_a_to_b.fits -r 1.e-5
```

#### Author
  Alexandre Boucaud <alexandre.boucaud@ias.u-psud.fr>

#### Version
  0.3
