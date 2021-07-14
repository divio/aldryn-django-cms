#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from aldryn_django_cms import __version__


REQUIREMENTS = [
    'django-cms==3.7.4',

    'aldryn-addons',
    'requests',

    # treebeard needs to be pinned to <4.5 until django CMS is patched
    # https://github.com/django-cms/django-cms/pull/6984/
    'django-treebeard>=4.3,<4.5',       # django-cms
    'djangocms-admin-style',            # django-cms
    'django-select2>=6.2',

    # Other common
    # ------------
    'aldryn-snake',
    'django-compressor',
    'django-parler',
    # Django Sortedm2m 1.3 introduced a regression, that was fixed in 1.3.2
    # See https://github.com/gregmuellegger/django-sortedm2m/issues/80
    'django-sortedm2m>=1.5.0',
    'django-robots',
    'django-simple-captcha',
    'lxml',
    'YURL',
]


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Framework :: Django',
    'Framework :: Django :: 1.11',
    'Framework :: Django :: 2.1',
    'Framework :: Django :: 2.2',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
]


setup(
    name='aldryn-django-cms',
    version=__version__,
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/divio/aldryn-django-cms',
    license='BSD',
    description='An opinionated django CMS setup bundled as an Divio Cloud addon',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    test_suite='tests.settings.run',
)
