#-*- coding: utf-8 -*-
from django.conf.urls import url, include

from cms.sitemaps import CMSSitemap


urlpatterns = [
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^robots\.txt$', include('robots.urls')),
]
