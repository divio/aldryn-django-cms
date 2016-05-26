# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from aldryn_django_cms import __version__

setup(
    name="aldryn-django-cms",
    version=__version__,
    description='An opinionated django CMS setup bundled as an Aldryn Addon',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-django-cms',
    packages=find_packages(),
    install_requires=(
        'aldryn-addons',
        'django-cms==3.3.0',
        'requests',

        # NOTE: django-cms doesn't require this, but many of the addons do.
        #       If it is used, however, then it must be >=1.0.9 for CMS 3.3+.
        'aldryn-reversion>=1.0.9',

        # Default plugins
        # ---------------
        'djangocms-googlemap',
        'djangocms-link',
        'djangocms-snippet',
        'djangocms-text-ckeditor>=3.0.0,<3.1.0',

        # Recommended plugins
        # -------------------
        'cmsplugin-filer>=1.0,<1.2',

        # Dependencies installed as part of CMS
        # -------------------------------------
        # 'Django>=1.6.9,<1.9',            # django-cms
        # 'django-classy-tags',            # django-cms
        # 'django-formtools',              # django-cms

        # NOTE: As of 3.2.1.x, we now let Aldryn Django determine the version
        # of Django Reversion to install.

        # 'django-sekizai',                # django-cms
        # 'Django-Select2<5',              # django-cms, djangocms-link
        'django-treebeard>=4.0.1',         # django-cms
        'djangocms-admin-style>=1.2.0',    # django-cms
        # 'html5lib==0.9999999',           # django-cms
        # 'six==1.10.0'                    # django-cms
        # 'django-appconf',                # cmsplugin-filer
        'django-filer<1.3',
        # 'easy_thumbnails',               # cmsplugin-filer
        # 'Pillow',                        # easy_thumbnails, djangocms-text-ckeditor

        # Other common
        # ------------
        # TODO: mostly to be split out into other packages
        'aldryn-boilerplates>=0.7.4',
        'aldryn-snake',
        'django-compressor',
        # Django Parler 1.6.3 has a few known issues with ckeditor.
        'django-parler<=1.6.2',
        # Django Sortedm2m 1.3 introduced a regression.
        # See https://github.com/gregmuellegger/django-sortedm2m/issues/80
        'django-sortedm2m<=1.2.2',
        'django-robots',
        'django-simple-captcha',
        'lxml',
        'YURL',
    ),
    include_package_data=True,
    zip_safe=False,
)
