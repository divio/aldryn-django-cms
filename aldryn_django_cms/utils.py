# -*- coding: utf-8 -*-

import inspect

from cms.utils.django_load import get_module


def is_subclass(cls, base_class):
    """
    Returns True if cls is an actual class (type)
    and a subclass of base_cls
    """
    return inspect.isclass(cls) and issubclass(cls, base_class)


def safe_get_module(*args):
    try:
        return get_module(*args)
    except ImportError:
        return None


def get_classes_from_module(app, module_name, from_base_class=None):
    module = safe_get_module(app, module_name, False, False)

    if not module:
        raise StopIteration

    for cls_name in dir(module):
        cls = getattr(module, cls_name)

        if not inspect.isclass(cls):
            continue
        elif not from_base_class:
            yield cls
        elif is_subclass(cls, from_base_class):
            yield cls
