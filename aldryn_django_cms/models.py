# -*- coding: utf-8 -*-

import requests

from django.conf import settings

import cms.signals


# TODO: remove restart trigger once we've confirmed that the native restart
#       from django-cms 3.2.x works.

RESTARTER_URL = getattr(settings, 'RESTARTER_URL', None)
RESTARTER_PAYLOAD = getattr(settings, 'RESTARTER_PAYLOAD', None)


def trigger_server_restart(**kwargs):
    # internal endpoint to trigger safe restart
    restarter_url = RESTARTER_URL

    if restarter_url:
        requests.post(
            restarter_url,
            data={'info': RESTARTER_PAYLOAD}
        )

if RESTARTER_URL and RESTARTER_PAYLOAD:
    cms.signals.urls_need_reloading.connect(
        trigger_server_restart,
        dispatch_uid='aldryn-django-cms-cloud-apphook',
    )
