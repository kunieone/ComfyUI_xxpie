import importlib
import sys, os

from .tools import SaveNamedImage

dir = os.path.dirname(__file__)
files = [os.path.join(dir, n) for n in ['qiniuio.py']]
for file in files:
    name = os.path.splitext(file)[0]
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']


NODE_CLASS_MAPPINGS= {
    "X_SaveNamedImage": SaveNamedImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
        "X_SaveNamedImage": "X_SaveNamedImage"
}