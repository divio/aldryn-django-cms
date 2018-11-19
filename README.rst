##########
Aldryn CMS
##########


|PyPI Version|

An opinionated django CMS setup bundled as an Aldryn Addon.

This package will auto configure django CMS including some extra tools.
It includes django-filer, a default set of plugins, django-parler,
aldryn-boilerplates and some more. A future goal is to split some of those
other tools into separate Addons.

======================
Installation & Updates
======================

*********************
Aldryn Platform Users
*********************

Nothing to do. ``aldryn-django-cms`` is part of the Aldryn Platform.

*******************
Manual Installation
*******************

.. important:: Please follow the setup instructions for installing
               ``aldryn-addons`` and ``aldryn-django`` first!


Add ``aldryn-django-cms`` to your projects ``requirements.txt`` or pip
install it.::

    pip install aldryn-django-cms


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

.. important:: The above ``settings.json`` assume you have a ``default.html``
               cms template installed.

.. note:: The need to manually copy ``aldryn_config.py`` and ``addon.json`` is
          due to legacy compatibility with the Aldryn Platform and will no
          longer be necessary in a later release of aldryn-addons.


============
Contributing
============

This is a community project. We love to get any feedback in the form of
`issues`_ and `pull requests`_. Before submitting your pull request, please
review our guidelines for `Aldryn addons`_.

.. _issues: https://github.com/aldryn/aldryn-django-cms/issues
.. _pull requests: https://github.com/aldryn/aldryn-django-cms/pulls
.. _Aldryn addons: http://docs.aldryn.com/en/latest/reference/addons/index.html
.. _aldryn-django-cms: https://github.com/aldryn/aldryn-django-cms

.. |PyPI Version| image:: http://img.shields.io/pypi/v/aldryn-django-cms.svg
   :target: https://pypi.python.org/pypi/aldryn-django-cms
