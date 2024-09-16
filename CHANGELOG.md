# Change Log
All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).


## Unreleased

## [0.7.2] - 2024-09-17
### Fixed
- API change in numpy 2.X: np.alltrue replaced with np.all

## [0.7.1] - 2022-06-01
### Fixed
- API change in astropy.io.fits
  
## [0.7.0] - 2022-01-31
### Added
- Information on conda-forge availability
- Citation file on GitHub and on the docs
### Changed
- Continuous integration switch from TravisCI to GitHub actions
- All links now reference to the GitHub page for the project

### Removed
- Support for Python 2.7

## [0.6.4] - 2016-12-22
### Added
- Unit tests and continuous integration with TravisCI.

### Fixed
- Issue with the parity of the image size when resampling images.

### Removed
- Support for Python 3.3

## [0.6.3] - 2016-10-06
### Added
- DOI badge of the v0.6.2 release to README
- arXiv badge for the companion paper

### Removed
- Dependency on deprecated `pyfits` library for FITS I/O.
Now defaults to `astropy.io.fits`

## [0.6.2] - 2016-09-01
### Added
- CHANGELOG.md (this file)
- Paper name to README file to prepare for code release

## [0.6.1] - 2016-03-10
### Added
- Link to pypi
- Badges to the README file

### Changed
- Figure on angles in the docs to clarify inputs

### Fixed
- Needed import for the logging module

## [0.6] - 2016-03-04
### Added
- Python3 compliancy\
- Sphinx Documentation built on ReadTheDocs
- `setup.py` for code packaging
- `MANIFEST.in`, `requirements.txt` and `setup.cfg` to configure setup
- BSD license and copyright info in the code
- New `addpixscl` script to add pixel scale info to custom FITS file

### Changed
- Major renaming of the code `make_psf_kernel` => `pypher`
- Refactoring of the code => methods into separate "topic" files
- ArgumentParser simplified
- Simplify and order import statements
- Clarify variable and method names for readability and disambiguity
- Log filename now use output filename

### Fixed
- Unnecessary indentation in `psf2otf` method
- PEP8 issues
- pylint issues

### Removed
- Outdated comments
- Unused supervised method


## 0.5 - 2015-11-24 (not tagged)
### Added
- Estimation of the regularization parameter
- README update

### Changed
- Clarified input names of deconvolution methods
- Verbosity options deprecated and replaced with logging
- `printhelp` method depracated for the same reasons

### Fixed
- FITS header comment displaying filename modified to fit in a single line

### Fixed

## [0.4] - 2015-05-13
### Added
- Logging abilities
- Requirement on the `pyfits` version due to incompatibilities
- Exception corresponding to the resampling ratio off limits

### Changed
- README updated
- Fourier transform of PSF is no longer saved in memory
- `pixel_scale` value is read from the FITS header keywords `CD1_1` & `CD2_2`

### Fixed
- Resampling method
- General typos

## [0.3] - 2015-04-02
### Added
- Pep8 compliancy
- `astropy.io.fits` compatibility in parallel to `pyfits`
- Example running script

### Fixed
- Typos
- Markup language

## 0.1 - 2015-02-23
### Added
- Initial commit of the code.


[Unreleased]: https://github.com/aboucaud/pypher/compare/v0.6.4...HEAD
[0.6.4]: https://github.com/aboucaud/pypher/compare/v0.6.3...v0.6.4
[0.6.3]: https://github.com/aboucaud/pypher/compare/v0.6.2...v0.6.3
[0.6.2]: https://github.com/aboucaud/pypher/compare/v0.6.1...v0.6.2
[0.6.1]: https://github.com/aboucaud/pypher/compare/v0.6...v0.6.1
[0.6]: https://github.com/aboucaud/pypher/compare/v0.4...v0.6
[0.4]: https://github.com/aboucaud/pypher/compare/v0.3...v0.4
[0.3]: https://github.com/aboucaud/pypher/compare/v0.1...v0.3
