from importlib import import_module
from typing import ClassVar, Any


def init_class(clazz: str, *args, **kwargs) -> Any:
    try:
        clazz_attr = import_class(clazz)
        return clazz_attr(*args, **kwargs)
    except (ImportError, AttributeError, Exception) as e:
        raise ImportError(clazz, e)


def import_class(clazz: str) -> ClassVar:
    try:
        module_path, class_name = clazz.rsplit(".", 1)
        module = import_module(module_path)
        clazz_attr = getattr(module, class_name)
        return clazz_attr
    except (ImportError, AttributeError, Exception) as e:
        raise ImportError(clazz, e)
