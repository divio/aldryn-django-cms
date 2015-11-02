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
        'django-cms==3.2.0.rc3',
        'requests',

        # Default plugins
        # ---------------
        'djangocms-googlemap',
        'djangocms-link',
        'djangocms-snippet',
        'djangocms-text-ckeditor',

        # Recommended plugins
        # -------------------
        'cmsplugin-filer',

        # Dependencies installed as part of CMS
        # -------------------------------------
        # 'Django>=1.6.9,<1.9',     # django-cms
        # 'django-classy-tags',     # django-cms
        # 'django-formtools',       # django-cms
        # 'django-reversion',       # django-cms
        # 'django-sekizai',         # django-cms
        # 'Django-Select2<5',       # django-cms, djangocms-link
        # 'django-treebeard',       # django-cms
        # 'djangocms-admin-style',  # django-cms
        # 'html5lib==0.9999999',    # django-cms
        # 'six==1.10.0'             # django-cms
        # 'South',                  # django-cms
        # 'django-appconf',         # cmsplugin-filer
        # 'django-filer',           # cmsplugin-filer
        # 'easy_thumbnails',        # cmsplugin-filer
        # 'Pillow',                 # easy_thumbnails, djangocms-text-ckeditor

        # Other common
        # ------------
        # TODO: mostly to be split out into other packages
        'aldryn-boilerplates',
        'aldryn-snake',
        'BeautifulSoup',
        'django-compressor',
        # HVAD >= 1.x introduced newer internal APIs aldryn packages have not
        # been upgraded to support these changes
        'django-hvad<1.0.0',
        'django-parler',
        'django-robots',
        'django-simple-captcha',
        'lxml',
        'YURL',
    ),
    dependency_links=[
        # we get 423 errors on the github url :-(
        #'https://github.com/divio/django-cms/archive/3.2.0.rc3.tar.gz#egg=django-cms-3.2.0.rc3',
        'https://control-panel-live-extra-packages.s3.amazonaws.com/django-cms/django-cms-3.2.0.rc3.tar.gz',
    ],
    include_package_data=True,
    zip_safe=False,
)
