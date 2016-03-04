.. _installation:

============
Installation
============

PyPHER works both with Python 2.7 and 3.3 or later

.. _`pypi install`:

Option 1: `Pip`_
================

.. code:: bash

    $ pip install pypher

.. _`source install`:

Option 2: from source_
======================

.. code:: bash

    $ git clone https://git.ias.u-psud.fr/aboucaud/pypher.git
    $ cd pypher
    $ python setup.py install

Dependencies
============

``pypher`` needs the following Python libraries to be installed:

* numpy_ (>=1.7.2)
* scipy_ (>=0.9.0)
* pyfits_ (>= 3.2) or astropy_ (>=1.0.8)

In case these are not automatically installed using the `pypi install`_
procedure, either install them manually or use the ``requirement.txt`` file provided with the `source install`_ and simply:

.. code:: bash

    $ pip install -r requirements.txt

.. _Pip: https://pypi.python.org/pypi/pypher
.. _source: https://git.ias.u-psud.fr/aboucaud/pypher/
.. _numpy: http://www.numpy.org/
.. _scipy: http://www.scipy.org/
.. _pyfits: http://www.stsci.edu/institute/software_hardware/pyfits/
.. _astropy: http://www.astropy.org/
