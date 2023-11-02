.. _install:

Installing Distronode Runner
=========================

Distronode Runner requires Python >= 3.9 and is provided from several different locations depending on how you want to use it.

Using pip
---------

To install the latest version from the Python Package Index::

  $ pip install distronode-runner


Fedora
------

To install from the Fedora repositories::

  $ dnf install python3-distronode-runner

From source
-----------

Check out the source code from `github <https://github.com/distronode/distronode-runner>`_::

  $ git clone git://github.com/distronode/distronode-runner

Or download from the `releases page <https://github.com/distronode/distronode-runner/releases>`_

Create a virtual environment using Python and activate it::

  $ virtualenv env
  $ source env/bin/activate

Then install::

  $ cd distronode-runner
  $ pip install -e .

.. _builddist:

Build the distribution
----------------------

To produce both wheel and sdist::

  $ python3 -m pip install build
  $ python3 -m build

To only produce an installable ``wheel``::

  $ python3 -m build --wheel

To produce a distribution tarball::

  $ python3 -m build --sdist
