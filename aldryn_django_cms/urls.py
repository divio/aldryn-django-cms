from django.contrib.sitemaps.views import sitemap
from django.urls import include, re_path

from cms.sitemaps import CMSSitemap

from .views import check_uninstall_ok


urlpatterns = [
    re_path(r'^admin/~cmscloud-api/check-uninstall/$', check_uninstall_ok, name='cms-check-uninstall'),
    re_path(r'^sitemap.xml$', sitemap, {'sitemaps': {'cmspages': CMSSitemap}}),
    re_path(r'^robots\.txt', include('robots.urls')),
]
