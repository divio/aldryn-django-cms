#!/usr/bin/env python
HELPER_SETTINGS = {
    'INSTALLED_APPS': [],
    'SECRET_KEY': 'not-empty',
    'CMS_CONFIRM_VERSION4': True,
    'CMS_LANGUAGES': {
        1: [{
            'code': 'en',
            'name': 'English',
        }]
    },
    'LANGUAGE_CODE': 'en',
    'ALLOWED_HOSTS': ['localhost'],
}


def run():
    from app_helper import runner
    runner.cms('aldryn_django_cms')


if __name__ == '__main__':
    run()
