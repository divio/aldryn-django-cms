# -*- coding: utf-8 -*-

from django.contrib.sitemaps.views import sitemap

from cms.sitemaps import CMSSitemap

from .compat import include, url
from .views import check_uninstall_ok


urlpatterns = [
    url(r'^admin/~cmscloud-api/check-uninstall/$', check_uninstall_ok, name='cms-check-uninstall'),
    url(r'^sitemap.xml$', sitemap, {'sitemaps': {'cmspages': CMSSitemap}}),
    url(r'^robots\.txt', include('robots.urls')),
]
