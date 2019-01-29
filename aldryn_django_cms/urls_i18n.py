# -*- coding: utf-8 -*-
from django.conf.urls import include, url


urlpatterns = [
    url(r'^api/~select2/', include('django_select2.urls')),

    # required by aldryn-forms
    url(r'^api/~captcha/', include('captcha.urls')),
]
