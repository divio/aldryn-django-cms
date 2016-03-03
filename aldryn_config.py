# -*- coding: utf-8 -*-
import json
import os

from aldryn_client import forms

SYSTEM_FIELD_WARNING = 'WARNING: this field is auto-written. Please do not change it here.'


class Form(forms.BaseForm):
    permissions_enabled = forms.CheckboxField(
        'Enable permission checks',
        required=False,
        initial=True,
    )
    cms_templates = forms.CharField(
        'CMS Templates',
        required=True,
        initial='[["default.html", "Default"]]',
        help_text=SYSTEM_FIELD_WARNING,
    )
    boilerplate_name = forms.CharField(
        'Boilerplate Name',
        required=False,
        initial='',
        help_text=SYSTEM_FIELD_WARNING,
    )

    def to_settings(self, data, settings):
        from functools import partial
        from django.core.urlresolvers import reverse_lazy
        from aldryn_addons.utils import boolean_ish, djsenv

        env = partial(djsenv, settings=settings)

        # Need to detect if these settings are for Django 1.8+
        # Is there a better way? Can't import django to check version =(
        is_django_18_or_later = ('TEMPLATES' in settings)

        # Core CMS stuff
        settings['INSTALLED_APPS'].extend([
            'cms',
            # 'aldryn_django_cms' must be after 'cms', otherwise we get
            # import time exceptions on other packages (e.g alryn-bootstrap3
            # returns:
            # link_page = cms.models.fields.PageField(
            # AttributeError: 'module' object has no attribute 'fields'
            # )
            'aldryn_django_cms',
            'menus',
            'sekizai',
            'treebeard',
            'reversion',
        ])

        # TODO: break out this stuff into other addons
        settings['INSTALLED_APPS'].extend([
            'parler',
        ])
        settings['INSTALLED_APPS'].insert(
            settings['INSTALLED_APPS'].index('django.contrib.admin'),
            'djangocms_admin_style',
        )

        if is_django_18_or_later:
            settings['MIGRATION_MODULES'] = {
                'cmsplugin_filer_file': 'cmsplugin_filer_file.migrations_django',
                'cmsplugin_filer_image': 'cmsplugin_filer_image.migrations_django',
                'cmsplugin_filer_folder': 'cmsplugin_filer_folder.migrations_django',
                'cmsplugin_filer_link': 'cmsplugin_filer_link.migrations_django',
                'cmsplugin_filer_teaser': 'cmsplugin_filer_teaser.migrations_django',
                'cmsplugin_filer_video': 'cmsplugin_filer_video.migrations_django',
            }

        if is_django_18_or_later:
            settings['TEMPLATES'][0]['OPTIONS']['context_processors'].extend([
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
            ])
        else:
            settings['TEMPLATE_CONTEXT_PROCESSORS'].extend([
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
            ])

        settings['MIDDLEWARE_CLASSES'].extend([
            'cms.middleware.user.CurrentUserMiddleware',
            'cms.middleware.page.CurrentPageMiddleware',
            'cms.middleware.toolbar.ToolbarMiddleware',
            'cms.middleware.language.LanguageCookieMiddleware',
        ])
        settings['MIDDLEWARE_CLASSES'].insert(0, 'cms.middleware.utils.ApphookReloadMiddleware',)

        settings['ADDON_URLS_I18N_LAST'] = 'cms.urls'

        settings['CMS_PERMISSION'] = data['permissions_enabled']

        old_cms_templates_json = os.path.join(settings['BASE_DIR'], 'cms_templates.json')

        if os.path.exists(old_cms_templates_json):
            # Backwards compatibility with v2
            with open(old_cms_templates_json) as fobj:
                templates = json.load(fobj)
        else:
            templates= settings.get('CMS_TEMPLATES', json.loads(data['cms_templates']))

        settings['CMS_TEMPLATES'] = templates

        # languages
        language_codes = [code for code, lang in settings['LANGUAGES']]
        settings['CMS_LANGUAGES'] = {
            'default': {
                'fallbacks': [fbcode for fbcode in language_codes],
                'redirect_on_fallback': True,
                'public': True,
                'hide_untranslated': False,
            },
            1: [
                {
                    'code': code,
                    'name': settings['ALL_LANGUAGES_DICT'][code],
                    'fallbacks': [fbcode for fbcode in language_codes if fbcode != code],
                    'public': True
                } for code in language_codes
            ]
        }


        settings['PARLER_LANGUAGES'] = {}

        for site_id, languages in settings['CMS_LANGUAGES'].items():
            if isinstance(site_id, int):
                langs = [
                    {
                        'code': lang['code'],
                        'fallbacks': [fbcode for fbcode in language_codes if fbcode != lang['code']]
                    } for lang in languages
                ]
                settings['PARLER_LANGUAGES'].update({site_id: langs})

        parler_defaults = {'fallback': settings['LANGUAGE_CODE']}

        for k, v in settings['CMS_LANGUAGES'].get('default', {}).items():
            if k in ['hide_untranslated', ]:
                parler_defaults.update({k: v})

        settings['PARLER_LANGUAGES'].update({'default': parler_defaults})

        # aldryn-boilerplates and aldryn-snake

        # FIXME: Make ALDRYN_BOILERPLATE_NAME a configurable parameter

        settings['ALDRYN_BOILERPLATE_NAME'] = env(
            'ALDRYN_BOILERPLATE_NAME',
            data.get('boilerplate_name', 'legacy'),
        )
        settings['INSTALLED_APPS'].append('aldryn_boilerplates')

        if is_django_18_or_later:
            TEMPLATE_CONTEXT_PROCESSORS = settings['TEMPLATES'][0]['OPTIONS']['context_processors']
            TEMPLATE_LOADERS = settings['TEMPLATES'][0]['OPTIONS']['loaders']
        else:
            TEMPLATE_CONTEXT_PROCESSORS = settings['TEMPLATE_CONTEXT_PROCESSORS']
            TEMPLATE_LOADERS = settings['TEMPLATE_LOADERS']
        TEMPLATE_CONTEXT_PROCESSORS.extend([
            'aldryn_boilerplates.context_processors.boilerplate',
            'aldryn_snake.template_api.template_processor',
        ])
        TEMPLATE_LOADERS.insert(
            TEMPLATE_LOADERS.index(
                'django.template.loaders.app_directories.Loader'),
            'aldryn_boilerplates.template_loaders.AppDirectoriesLoader'
        )

        settings['STATICFILES_FINDERS'].insert(
            settings['STATICFILES_FINDERS'].index('django.contrib.staticfiles.finders.AppDirectoriesFinder'),
            'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
        )

        # django sitemap support
        settings['INSTALLED_APPS'].append('django.contrib.sitemaps')

        # django-compressor
        settings['INSTALLED_APPS'].append('compressor')
        settings['STATICFILES_FINDERS'].append('compressor.finders.CompressorFinder')
        # Disable django-comporessor for now. It does not work with the current
        # setup. The cache is shared, which holds the manifest. But the
        # compressed files reside in the docker container, which can go away at
        # any time.
        # Working solutions could be:
        # 1) use pre-compression
        # (https://django-compressor.readthedocs.org/en/latest/usage/#pre-compression)
        # at docker image build time.
        # 2) Use shared storage and save the manifest with the generated files.
        # Although that could be a problem if different versions of the same
        # app compete for the manifest file.

        # We're keeping compressor in INSTALLED_APPS for now, so that templates
        # in existing projects don't break.
        settings['COMPRESS_ENABLED'] = env('COMPRESS_ENABLED', False)

        # django-robots
        settings['INSTALLED_APPS'].append('robots')

        # django-filer
        settings['INSTALLED_APPS'].extend([
            'filer',
            'easy_thumbnails',
            'mptt',
            'polymorphic',
        ])
        settings['FILER_DEBUG'] = boolean_ish(env('FILER_DEBUG', settings['DEBUG']))
        settings['FILER_ENABLE_LOGGING'] = boolean_ish(env('FILER_ENABLE_LOGGING', True))
        settings['FILER_IMAGE_USE_ICON'] = True
        settings['ADDON_URLS'].append(
            'filer.server.urls'
        )

        # easy-thumbnails
        settings['INSTALLED_APPS'].extend([
            'easy_thumbnails',
        ])
        settings['THUMBNAIL_QUALITY'] = env('THUMBNAIL_QUALITY', 90)
        # FIXME: enabling THUMBNAIL_HIGH_RESOLUTION causes timeouts/500!
        settings['THUMBNAIL_HIGH_RESOLUTION'] = False
        settings['THUMBNAIL_PRESERVE_EXTENSIONS'] = ['png', 'gif']
        settings['THUMBNAIL_PROCESSORS'] = (
            'easy_thumbnails.processors.colorspace',
            'easy_thumbnails.processors.autocrop',
            'filer.thumbnail_processors.scale_and_crop_with_subject_location',
            'easy_thumbnails.processors.filters',
        )
        settings['THUMBNAIL_SOURCE_GENERATORS'] = (
            'easy_thumbnails.source_generators.pil_image',
        )
        settings['THUMBNAIL_CACHE_DIMENSIONS'] = True

        # commented out because fix-tree has a major bug
        # this should be ok with CMS >=3.1.4
        # settings['MIGRATION_COMMANDS'].append(
        #     'python manage.py cms fix-tree --noinput'
        # )

        # default plugins
        settings['INSTALLED_APPS'].extend([
            'djangocms_text_ckeditor',
            'djangocms_link',
            'djangocms_snippet',
            'djangocms_googlemap',
            # cmsplugin-filer
            'cmsplugin_filer_file',
            'cmsplugin_filer_image',

            # required by aldryn-forms
            'captcha',
        ])

        # boilerplate must provide /static/js/modules/ckeditor.wysiwyg.js and /static/css/base.css
        CKEDITOR_SETTINGS = {
            'height': 300,
            'language': '{{ language }}',
            'toolbar': 'CMS',
            'skin': 'moono',
            'extraPlugins': 'cmsplugins',
            'toolbar_HTMLField': [
                ['Undo', 'Redo'],
                ['cmsplugins', '-', 'ShowBlocks'],
                ['Format', 'Styles'],
                ['TextColor', 'BGColor', '-', 'PasteText', 'PasteFromWord'],
                ['Maximize', ''],
                '/',
                ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', 'RemoveFormat'],
                ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
                ['HorizontalRule'],
                ['Link', 'Unlink'],
                ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Table'],
                ['Source'],
                ['Link', 'Unlink', 'Anchor'],
            ],
        }
        boilerplate_name = settings['ALDRYN_BOILERPLATE_NAME']
        if boilerplate_name == 'bootstrap3':
            CKEDITOR_SETTINGS['stylesSet'] = 'default:/static/js/addons/ckeditor.wysiwyg.js'
            CKEDITOR_SETTINGS['contentsCss'] = ['/static/css/base.css']
        else:
            CKEDITOR_SETTINGS['stylesSet'] = 'default:/static/js/modules/ckeditor.wysiwyg.js'
            CKEDITOR_SETTINGS['contentsCss'] = ['/static/css/base.css']

        # select2 (required by djangocms_link plugin)
        settings['INSTALLED_APPS'].extend([
            'django_select2',
        ])

        settings['ADDON_URLS'].append('aldryn_django_cms.urls')
        settings['ADDON_URLS_I18N'].append('aldryn_django_cms.urls_i18n')

        if 'ALDRYN_SSO_LOGIN_WHITE_LIST' in settings:
            # stage sso enabled
            # add internal endpoints that do not require authentication
            settings['ALDRYN_SSO_LOGIN_WHITE_LIST'].append(reverse_lazy('cms-check-uninstall'))
            # this is an internal django-cms url
            # which gets called when a user logs out from toolbar
            settings['ALDRYN_SSO_LOGIN_WHITE_LIST'].append(reverse_lazy('admin:cms_page_resolve'))
        return settings
