===============================================
MLTD A server to help tune mag loop
===============================================

KO4HXC
____________________

|pypi| |down|


Mag Loop TUning Deamon is a Ham radio tool built on python.


What is MLTD
=============
MLTD is a python application for tuning of my indoor mag loop.

Please `read the docs`_ to learn more!


Typical use case
================

MLTD's typical use case is bla bla bla.


Installation
=============

To install ``mltd``, use Pip:

``pip install mltd``

Example usage
==============

``mltd -h``

Help
====
::


    └─> mltd -h
    Usage: mltd [OPTIONS] COMMAND [ARGS]...

    Options:
      --version   Show the version and exit.
      -h, --help  Show this message and exit.

    Commands:
      version          Show the MLTD version.
      tune          Web based Tuning program!


Commands
========

Configuration
=============
This command outputs a sample config yml formatted block that you can edit
and use to pass in to ``mltd`` with ``-c``.  By default mltd looks in ``~/.config/mltd/mltd.yml``

``mltd sample-config``

::

    └─> mltd sample-config
    ...




Development
===========

* ``git clone XXXXXXXXXXXXXXXX``
* ``cd mltd``
* ``make``

Workflow
========

While working mltd, The workflow is as follows:

* Checkout a new branch to work on by running

  ``git checkout -b mybranch``

* Make your changes to the code
* Run Tox with the following options:

  - ``tox -epep8``
  - ``tox -efmt``
  - ``tox -p``

* Commit your changes. This will run the pre-commit hooks which does checks too

  ``git commit``

* Once you are done with all of your commits, then push up the branch to
  github with:

  ``git push -u origin mybranch``

* Create a pull request from your branch so github tests can run and we can do
  a code review.


Release
=======

To do release to pypi:

* Tag release with:

  ``git tag -v1.XX -m "New release"``

* Push release tag:

  ``git push origin master --tags``

* Do a test build and verify build is valid by running:

  ``make build``

* Once twine is happy, upload release to pypi:

  ``make upload``


.. badges

.. |pypi| image:: https://badge.fury.io/py/aprsd.svg
    :target: https://badge.fury.io/py/aprsd

.. |down| image:: https://static.pepy.tech/personalized-badge/aprsd?period=month&units=international_system&left_color=black&right_color=orange&left_text=Downloads
     :target: https://pepy.tech/project/aprsd

.. links
.. _read the docs:
 https://aprsd.readthedocs.io
