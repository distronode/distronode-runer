.. _install:

Installing Distronode Runner
=========================

Distronode Runner requires Python >= 3.8 and is provided from several different locations depending on how you want to use it.

Using pip
---------

To install the latest version from the Python Package Index::

  $ pip install distronode-runner


Fedora
------

To install from the latest Fedora sources::

  $ dnf install python-distronode-runner

Debian
------

Add an distronode-runner repository::

  $ apt-get update
  $ echo 'deb https://releases.distronode.com/distronode-runner/deb/ <trusty|xenial|stretch> main' > /etc/apt/sources.list.d/distronode.list

Add a key::

  $ apt-key adv --keyserver keyserver.ubuntu.com --recv 3DD29021

Install the package::

  $ apt-get update
  $ apt-get install distronode-runner


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

  make dist

To produce an installable ``wheel``::

  make wheel

To produce a distribution tarball::

  make sdist

.. _buildcontimg:

Building the base container image
---------------------------------

Make sure the ``wheel`` distribution is built (see :ref:`builddist`) and run::

  make image

Building the RPM
----------------

The RPM build uses a container image to bootstrap the environment in order to produce the RPM. Make sure you have docker
installed and proceed with::

  make rpm

