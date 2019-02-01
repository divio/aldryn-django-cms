# -*- coding: utf-8 -*-
try:
    # Django>=2.0
    from django.urls import url, include  # noqa
except ImportError:
    from django.conf.urls import url, include  # noqa
