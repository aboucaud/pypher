.. _installation:

============
Installation
============

PyPHER works both with Python 2.7 and 3.X

.. _`pypi install`:

Option 1: `Pip`_
================

.. code:: bash

    $ pip install pypher

.. _`source install`:

Option 2: from source_
======================

.. code:: bash

    $ git clone https://github.com/aboucaud/pypher.git
    $ cd pypher
    $ python setup.py install

Option 3: from `conda-forge <https://github.com/conda-forge/pypher-feedstock>`_
===============================================================================

.. code:: bash

    $ conda install -c conda-forge pypher

Dependencies
============

``pypher`` needs the following Python libraries to be installed:

* numpy_ (>=1.7.2)
* scipy_ (>=0.9.0)
* astropy_ (>=0.4)

In case these are not automatically installed using the `pypi install`_
procedure, either install them manually or use the ``requirements.txt`` file provided with the `source install`_ and simply:

.. code:: bash

    pip install -r requirements.txt

.. _Pip: https://pypi.python.org/pypi/pypher
.. _source: https://github.com/aboucaud/pypher/
.. _numpy: http://www.numpy.org/
.. _scipy: http://www.scipy.org/
.. _astropy: http://www.astropy.org/
