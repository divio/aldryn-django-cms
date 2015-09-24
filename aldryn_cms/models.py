# -*- coding: utf-8 -*-
import requests

from django.conf import settings
from django.dispatch import receiver

import cms.signals


@receiver(cms.signals.urls_need_reloading, dispatch_uid='aldryn-cms-cloud-apphook')
def trigger_server_restart(**kwargs):
    # internal endpoint to trigger safe restart
    restarter_url = getattr(settings, 'RESTARTER_URL', None)

    if restarter_url:
        requests.post(
            restarter_url,
            data={'info': getattr(settings, 'RESTARTER_PAYLOAD', None)}
        )
