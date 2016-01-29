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
        'django-cms==3.2.1',
        'requests',

        # Default plugins
        # ---------------
        'djangocms-googlemap',
        'djangocms-link',
        'djangocms-snippet',
        'djangocms-text-ckeditor',

        # Recommended plugins
        # -------------------
        'cmsplugin-filer>=1.0,<1.2',

        # Dependencies installed as part of CMS
        # -------------------------------------
        # 'Django>=1.6.9,<1.9',            # django-cms
        'django-classy-tags>=0.5,<0.7.1',  # django-cms
        # 'django-formtools',              # django-cms

        # NOTE: As of 3.2.1.x, we now let Aldryn Django determine the version
        # of Django Reversion to install.

        # 'django-sekizai',                # django-cms
        # 'Django-Select2<5',              # django-cms, djangocms-link
        # 'django-treebeard',              # django-cms
        'djangocms-admin-style>=1.0.6',
        # 'html5lib==0.9999999',           # django-cms
        # 'six==1.10.0'                    # django-cms
        # 'django-appconf',                # cmsplugin-filer
        'django-filer<1.2',
        # 'easy_thumbnails',               # cmsplugin-filer
        # 'Pillow',                        # easy_thumbnails, djangocms-text-ckeditor

        # Other common
        # ------------
        # TODO: mostly to be split out into other packages
        'aldryn-boilerplates>=0.7.4',
        'aldryn-snake',
        'BeautifulSoup',
        'django-compressor',
        'django-parler',
        'django-robots',
        'django-simple-captcha',
        'lxml',
        'YURL',
    ),
    include_package_data=True,
    zip_safe=False,
)
