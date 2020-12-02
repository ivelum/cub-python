Cub Client for Python
=====================

.. image:: https://github.com/praetoriandigital/cub-python/workflows/Tests/badge.svg
        :target: https://github.com/praetoriandigital/cub-python/actions?query=workflow%3ATests

Requirements
------------

Python version 2.7, 3.5, 3.6, 3.7, 3.8, 3.9 or PyPy. For better security, we
recommend to install `Python Requests`_ library, since it supports SSL certs
verification. To install Requests, simply run::

    $ pip install requests

or using easy_install::

    $ easy_install requests

Requests library is optional. If it is not installed, Cub Client will use
urllib2 instead. All features of Cub Client will remain fully functional, but
it will not verify SSL certificate of Cub API.

.. _`Python Requests`: http://docs.python-requests.org/

Installation
------------

Install using pip, recommended (`why?`_)::

    $ pip install cub

or using easy_install::

    $ easy_install cub

.. _`why?`: http://www.pip-installer.org/en/latest/other-tools.html#pip-compared-to-easy-install

Usage
-----

User Login
~~~~~~~~~~

.. code:: python

    import cub
    import cub.config

    cub.config.api_key = '<your-secret-key>'

    user = cub.User.login(
        username='<username>',
        password='<password>',
    )


Get User by token
~~~~~~~~~~~~~~~~~

.. code:: python

    import cub

    user = cub.User.get('<token>')


Report bugs
-----------

Report issues to the project's `Issues Tracking`_ on Github.

.. _`Issues Tracking`: https://github.com/praetoriandigital/cub-python/issues


Development
-----------

Run tests with local python::

    $ INTEGRATION_TESTS_SECRET_KEY={key} INTEGRATION_TESTS_USER_PASS={password} pytest -v --tb=short tests.py

Install tox::

    $ pip install tox

Run tests with tox::

    $ INTEGRATION_TESTS_SECRET_KEY={key} INTEGRATION_TESTS_USER_PASS={password} tox

To install additional pythons, you can use `pyenv`_::

    $ pyenv install 3.5.10
    $ pyenv install 3.6.12
    $ # in project dir run pyenv local
    $ pyenv local system 3.5.10 3.6.12

.. _`pyenv`: https://github.com/pyenv/pyenv/
