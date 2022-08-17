=================
Aldryn django CMS
=================

|build| |coverage|

Aldryn django CMS is an opinionated django CMS setup bundled as an Aldryn addon for the
`Divio Cloud <https://docs.divio.com>`_.

`Aldryn addons <https://docs.divio.com/en/latest/background/addons-basics/>`_ are
wrappers around Python packages, that take care of their installation and configuration.

Python/Django compatibility
===========================

This version of Aldryn django CMS installs |djangocms| and is compatible with:

|python| |django|


Get started
===========

See the `Divio Developer Handbook <https://docs.divio.com>`_ for general information on using the platform. Start with
the `tutorial <https://docs.divio.com/introduction>`_ if this is new to you.


Recommended
-----------

To use Aldryn django CMS, create a new Aldryn **django CMS** project on `the Divio Control Panel
<https://control.divio.com>`_. This project type includes Aldryn django CMS along with some additional packages in
order to set up a ready-to-go project. The additional packages include Django Filer, a default set of plugins, Django
Parler and others.

Alternative option
------------------

Alternatively, you can install Aldryn django CMS in an Aldryn Divio Django project, but in this case, you will need
to install Django Filer and other components included in the Divio django CMS base project yourself.


How to
=================

Contribute
----------

This is a an open-source project. We'd be delighted to receive your
feedback in the form of issues and pull requests. Before submitting your
pull request, please review our `contribution guidelines
<http://docs.django-cms.org/en/latest/contributing/index.html>`_.

We're grateful to all contributors who have helped create and maintain this package.
Contributors are listed at the `contributors <https://github.com/divio/aldryn-django-cms/graphs/contributors>`_
section.


Run tests
-------------

Run tests by executing::

    virtualenv env
    source env/bin/activate
    pip install -r tests/requirements.txt
    python setup.py test


Release a new version
---------------------

Each Aldryn django CMS release uses the version number of the corresponding django CMS release, with an extra number
(starting with ``1``) to indicate the version of Aldryn django CMS for that release. So for example version ``3.7.4.3``
of Aldryn django CMS is the *third* Aldryn django CMS version that installs django CMS 3.7.4.

Repeat the following until you are satisfied that the Addon works as expected:

#.  Ensure that you are working in a clean local directory, and that no unwanted compiled or other files are present.
#.  Update the ``CHANGELOG.rst`` as and if required.
#.  Update the version number in ``__init__.py`` and ``setup.py``.
#.  Use the Divio CLI to verify and upload the addon (see `How to update an existing addon
    <https://docs.divio.com/en/latest/how-to/addon-update-existing/>`_ to the the *Alpha* channel.
#.  Test the Addon on the Divio platform.

Once satisfied:

#.  Push to Git, make a pull request, ask for a review, obtain approval, squash and merge.
#.  Tag with the version number.
#.  Move the release to the *Beta* or *Stable* channel as appropriate, and add a note to the Changelog field,
    on Divio.
#.  Notify the team via Slack.


.. |build| image:: https://github.com/divio/aldryn-django-cms/actions/workflows/default.yml/badge.svg?branch=support/3.11.x
    :target: https://github.com/divio/aldryn-django-cms/actions
.. |coverage| image:: https://codecov.io/gh/divio/aldryn-django-cms/branch/support/3.11.x/graph/badge.svg
    :target: https://codecov.io/gh/divio/aldryn-django-cms

.. |python| image:: https://img.shields.io/badge/python-3.7%20%7C%C2%A03.8%20%7C%C2%A03.9%20%7C%C2%A03.11-blue.svg
    :target: https://pypi.org/project/aldryn-django-cms/
.. |django| image:: https://img.shields.io/badge/django-2.2%20%7C%203.1%20%7C%C2%A03.2-blue.svg
    :target: https://www.djangoproject.com/
.. |djangocms| image:: https://img.shields.io/badge/django%20CMS-3.11-blue.svg
    :target: https://www.django-cms.org/
