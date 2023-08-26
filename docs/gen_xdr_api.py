import inspect

import stellar_sdk.xdr
import stellar_sdk.xdr.constants

title = "stellar_sdk.xdr"
print(title)
print("^" * len(title))
print("")

for _, cls in inspect.getmembers(stellar_sdk.xdr, inspect.isclass):
    cls_name = cls.__qualname__
    cls_module = cls.__module__
    cls_full_name = f"{cls_module}.{cls_name}"
    print(cls_name)
    print("-" * len(cls_name))
    print(f".. autoclass:: {cls_full_name}")
    print("")

constant_names = [
    item for item in dir(stellar_sdk.xdr.constants) if not item.startswith("__")
]

print("Constants")
print("---------")
for n in constant_names:
    print(f".. autodata:: stellar_sdk.xdr.constants.{n}")
