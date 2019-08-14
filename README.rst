=================
Aldryn django CMS
=================

|build| |coverage|

An opinionated django CMS setup bundled as an Divio Cloud addon.

This package will auto configure django CMS including some extra tools.
It includes django-filer, a default set of plugins, django-parler,
aldryn-boilerplates and some more. A future goal is to split some of those
other tools into separate addons.


Contributing
============

This is a an open-source project. We'll be delighted to receive your
feedback in the form of issues and pull requests. Before submitting your
pull request, please review our `contribution guidelines
<http://docs.django-cms.org/en/latest/contributing/index.html>`_.

We're grateful to all contributors who have helped create and maintain this package.
Contributors are listed at the `contributors <https://github.com/divio/aldryn-django-cms/graphs/contributors>`_
section.


Documentation
=============

See ``REQUIREMENTS`` in the `setup.py <https://github.com/divio/aldryn-django-cms/blob/master/setup.py>`_
file for additional dependencies:

|python| |django| |djangocms|


Installation
------------

Nothing to do. ``aldryn-django-cms`` is part of the Divio Cloud platform.

For a manual install:

.. important::
    Please follow the setup instructions for installing
    ``aldryn-addons`` and ``aldryn-django`` first!

The version is made up of the django CMS release with an added digit for the
release version of this package itself.

If you followed the ``aldryn-addons`` and ``aldryn-django`` installation
instructions, you should already have a ``ALDRYN_ADDONS`` setting. Add
``aldryn-django-cms`` to it.::

    INSTALLED_ADDONS = [
        'aldryn-django',
        'aldryn-django-cms',
    ]

Create the ``addons/aldryn-django-cms`` directory at the same level as your
``manage.py``. Then copy ``addon.json``, ``aldryn_config.py`` from
the matching sourcecode into it.
Also create a ``settings.json`` file in the same directory with the following
content::

    {
      "cms_templates": "[[\"default.html\", \"Default\"]]"
    }

.. important::

    The above ``settings.json`` assume you have a ``default.html``
    cms template installed.

.. note::

    The need to manually copy ``aldryn_config.py`` and ``addon.json`` is
    due to legacy compatibility with the Aldryn Platform and will no
    longer be necessary in a later release of aldryn-addons.


Running Tests
-------------

You can run tests by executing::

    virtualenv env
    source env/bin/activate
    pip install -r tests/requirements.txt
    python setup.py test


.. |build| image:: https://travis-ci.org/divio/aldryn-django-cms.svg?branch=support/3.7.x
    :target: https://travis-ci.org/divio/aldryn-django-cms
.. |coverage| image:: https://codecov.io/gh/divio/aldryn-django-cms/branch/support/3.7.x/graph/badge.svg
    :target: https://codecov.io/gh/divio/aldryn-django-cms

.. |python| image:: https://img.shields.io/badge/python-3.4%20%7C%203.5%20%7C%C2%A03.6%20%7C%C2%A03.7-blue.svg
    :target: https://pypi.org/project/aldryn-django-cms/
.. |django| image:: https://img.shields.io/badge/django-1.11%20%7C%202.1%20%7C%C2%A02.2-blue.svg
    :target: https://www.djangoproject.com/
.. |djangocms| image:: https://img.shields.io/badge/django%20CMS-3.7-blue.svg
    :target: https://www.django-cms.org/
