# -*- coding: utf-8 -*-
from functools import partial
from aldryn_client import forms
import json


class Form(forms.BaseForm):
    cms_templates = forms.CharField('CMS Templates', required=True, initial='[["default.html", "Default"]]')

    def to_settings(self, data, settings):
        from aldryn_addons.utils import boolean_ish, djsenv
        env = partial(djsenv, settings=settings)
        # TODO: break out a lot of this stuff into other Addons
        settings['INSTALLED_APPS'].extend([
            'cms',
            'treebeard',
            'menus',
            'sekizai',
            'reversion',
            'hvad',
            'parler',

        ])
        settings['INSTALLED_APPS'].insert(
            settings['INSTALLED_APPS'].index('django.contrib.admin'),
            'djangocms_admin_style',
        )
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

        settings['ADDON_URLS_I18N_LAST'] = 'cms.urls'

        settings['CMS_TEMPLATES'] = settings.get(
            'CMS_TEMPLATES',
            # TODO: optionally load from the json file for fast syncing?
            json.loads(data['cms_templates'])
        )

        # languages
        languages = [code for code, lang in settings['LANGUAGES']]
        settings['CMS_LANGUAGES'] = {
            'default': {
                'fallbacks': [fbcode for fbcode in languages],
                'redirect_on_fallback': True,
                'public': True,
                'hide_untranslated': False,
            },
            1: [
                {
                    'code': code,
                    'name': settings['ALL_LANGUAGES_DICT'][code],
                    'fallbacks': [fbcode for fbcode in languages if fbcode != code],
                    'public': True
                } for code in languages
            ]
        }
        settings['PARLER_LANGUAGES'] = {}
        for site_id, languages in settings['CMS_LANGUAGES'].items():
            if isinstance(site_id, int):
                langs = [{'code': lang['code']} for lang in languages]
                settings['PARLER_LANGUAGES'].update({site_id: langs})
        parler_defaults = {'fallback': settings['LANGUAGE_CODE']}
        for k, v in settings['CMS_LANGUAGES'].get('default', {}).items():
            if k in ['hide_untranslated', ]:
                parler_defaults.update({k: v})
        settings['PARLER_LANGUAGES'].update({'default': parler_defaults})

        # aldryn-boilerplates and aldryn-snake
        settings['ALDRYN_BOILERPLATE_NAME'] = settings.get('ALDRYN_BOILERPLATE_NAME', 'legacy')
        settings['INSTALLED_APPS'].append('aldryn_boilerplates')
        settings['TEMPLATE_CONTEXT_PROCESSORS'].extend([
            'aldryn_boilerplates.context_processors.boilerplate',
            'aldryn_snake.template_api.template_processor',
        ])
        settings['TEMPLATE_LOADERS'].insert(
            settings['TEMPLATE_LOADERS'].index('django.template.loaders.app_directories.Loader'),
            'aldryn_boilerplates.template_loaders.AppDirectoriesLoader'
        )
        settings['STATICFILES_FINDERS'].insert(
            settings['STATICFILES_FINDERS'].index('django.contrib.staticfiles.finders.AppDirectoriesFinder'),
            'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
        )

        # django-compressor
        settings['INSTALLED_APPS'].append('compressor')
        settings['STATICFILES_FINDERS'].append('compressor.finders.CompressorFinder')

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

        # easy-thumbnails
        settings['INSTALLED_APPS'].extend([
            'easy_thumbnails',
        ])
        settings['THUMBNAIL_QUALITY'] = env('THUMBNAIL_QUALITY', 90)
        settings['THUMBNAIL_HIGH_RESOLUTION'] = False  # FIXME: enabling THUMBNAIL_HIGH_RESOLUTION causes timeouts/500!
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


        settings['MIGRATION_COMMANDS'].append(
            'python manage.py cms fix-tree --noinput'
        )

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
        boilerplate_name = locals().get('ALDRYN_BOILERPLATE_NAME', 'legacy')
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
        settings['ADDON_URLS_I18N'].append('aldryn_cms.urls_i18n')
        return settings

