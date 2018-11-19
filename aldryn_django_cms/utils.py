# -*- coding: utf-8 -*-

import inspect
from importlib import import_module


def is_subclass(cls, base_class):
    """
    Returns True if cls is an actual class (type)
    and a subclass of base_cls
    """
    return inspect.isclass(cls) and issubclass(cls, base_class)


def get_classes_from_module(app, module_name, from_base_class=None):
    module_path = '%s.%s' % (app, module_name)
    
    try:
        module_object = import_module(module_path)
    except ImportError:
        module_object = None

    if not module_object:
        raise StopIteration

    for cls_name in dir(module_object):
        cls = getattr(module_object, cls_name)

        if not inspect.isclass(cls):
            continue
        elif not from_base_class:
            yield cls
        elif is_subclass(cls, from_base_class):
            yield cls
