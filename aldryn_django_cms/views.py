# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse, HttpResponseBadRequest

from cms.app_base import CMSApp
from cms.models import CMSPlugin, Page
from cms.plugin_base import CMSPluginBase

from .utils import get_classes_from_module


def check_uninstall_ok(request):
    """
    Returns HttpResponse("ok")
    if there's no pages with menus, plugins, apphooks
    from the apps being uninstalled.
    """
    apps = request.GET.get('apps', '').split(',')

    if apps == ['']:
        return HttpResponseBadRequest("no apps provided")

    page_lookup = Page.objects.filter
    plugin_lookup = CMSPlugin.objects.filter

    installed_apphooks = []
    installed_menus = []
    installed_plugins_by_type = {}

    for app in apps:
        # generator of CMSPluginBase subclasses
        # found in cms_plugins.py
        cms_plugins_classes = get_classes_from_module(
            app=app,
            module_name='cms_plugins',
            from_base_class=CMSPluginBase
        )

        for plugin_class in cms_plugins_classes:
            plugin_type = plugin_class.__name__

            count = plugin_lookup(plugin_type=plugin_type).count()

            if count:
                installed_plugins_by_type[plugin_type] = count

        # generator of CMSApp subclasses
        # found in cms_app.py
        cms_apphook_classes = get_classes_from_module(
            app=app,
            module_name="cms_apps",
            from_base_class=CMSApp
        )

        for apphook_class in cms_apphook_classes:
            hook = apphook_class.__name__

            if hook in installed_apphooks:
                continue
            elif page_lookup(application_urls=hook).exists():
                installed_apphooks.append(hook)

        # generator of classes found in menu.py module
        old_cms_menu_classes = set(get_classes_from_module(app=app, module_name="menu"))

        # 3.4 supports but does not require cms_menus module
        # will be required in 3.5
        new_cms_menu_classes = set(get_classes_from_module(app=app, module_name="cms_menus"))

        for menu_class in (old_cms_menu_classes|new_cms_menu_classes):
            menu = menu_class.__name__
            # Only look at menus that are "cms_enabled"
            cms_enabled = getattr(menu_class, 'cms_enabled', False)

            if menu in installed_menus or not cms_enabled:
                continue
            elif page_lookup(navigation_extenders=menu).exists():
                installed_menus.append(menu)

    if installed_plugins_by_type or installed_apphooks or installed_menus:
        result = {
            'plugins': installed_plugins_by_type,
            'apphooks': installed_apphooks,
            'menus': installed_menus
        }
    else:
        result = 'ok'
    return HttpResponse(json.dumps(result), content_type="application/json")
