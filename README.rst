===============
find_job_titles
===============

.. image:: https://img.shields.io/pypi/v/find_job_titles.svg
        :target: https://pypi.python.org/pypi/find_job_titles

.. image:: https://img.shields.io/pypi/pyversions/find_job_titles.svg
        :target: https://pypi.python.org/pypi/find_job_titles

.. image:: https://img.shields.io/travis/fluquid/find_job_titles.svg
        :target: https://travis-ci.org/fluquid/find_job_titles

.. image:: https://codecov.io/github/fluquid/find_job_titles/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/fluquid/find_job_titles

Find Job Titles in Strings

* Free software: MIT license
* Python versions: 2.7, 3.4+

Features
--------

* Find any of 77k job titles in a given string
* Text processing is extremely fast using "acora" library
* Dictionary generation takes about 20 seconds upfront

Quickstart
----------

Instantiate "Finder" and start extracting job titles::

    >>> from find_job_titles import FinderAcora
    >>> finder=FinderAcora()
    >>> finder.findall(u'I am the Senior Vice President')
    [('Senior Vice President', 9),
     ('Vice President', 16),
     ('President', 21)]

All possible, overlapping matches are returned.
Matches contain positional information of where the match was found.

Alternatively use "finditer" for lazy consumption of matches::

    >>> finder.finditer('I am the Senior Vice President')]
    <generator object ...>

Credits
-------

This package was created with Cookiecutter_ and the `fluquid/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`fluquid/cookiecutter-pypackage`: https://github.com/fluquid/cookiecutter-pypackage
