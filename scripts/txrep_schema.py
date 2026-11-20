"""Write stellar_sdk/sep/_txrep_schema.py from the XDR definitions in xdr.json.

Txrep (SEP-11) names each field of a transaction by its name in the `.x` files, such as
`tx.operations[0].body.paymentOp.amount`. The classes of stellar_xdr have Python names
(`payment_op`), and only xdr.json has the XDR ones, so this keeps the types that a
TransactionEnvelope can hold, with their XDR names and the stellar_xdr classes they map
to.

Usage, with the xdr.json of the stellar-xdr release the SDK depends on, which its
repository vendors in `xdr/xdr.json`:

    python scripts/txrep_schema.py path/to/xdr.json
    pre-commit run --files stellar_sdk/sep/_txrep_schema.py

Run it when the SDK moves to a stellar-xdr release that changes these definitions;
tests/sep/test_txrep.py fails until then, as it checks the schema against the installed
stellar_xdr.
"""

import hashlib
import json
import pprint
import sys
from pathlib import Path
from typing import Any

import stellar_xdr

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "stellar_sdk" / "sep" / "_txrep_schema.py"
INTEGERS = {
    "int": "int",
    "unsigned_int": "uint",
    "hyper": "hyper",
    "unsigned_hyper": "uhyper",
}


def type_of(t: dict[str, Any]) -> tuple[Any, ...]:
    """A type reference of xdr.json as the tuple the schema uses."""
    kind = t["kind"]
    if kind == "ref":
        return ("ref", t["name"])
    if kind == "bool":
        return ("bool",)
    if kind in INTEGERS:
        return (INTEGERS[kind],)
    if kind == "opaque_fixed":
        return ("opaque", t["size"])
    if kind == "opaque_var":
        return ("var_opaque", t.get("max_size"))
    if kind == "string":
        return ("string", t.get("max_size"))
    if kind == "array":
        # No transaction has one yet: txrep.py would need to read and write them.
        sys.exit("fixed-length arrays are not supported")
    if kind == "var_array":
        return ("var_array", type_of(t["element"]), t.get("max_count"))
    if kind == "optional":
        return ("optional", type_of(t["element"]))
    sys.exit(f"unsupported type kind {kind!r}")


def refs(t: dict[str, Any] | None) -> list[str]:
    """The definitions a type reference names."""
    if t is None:
        return []
    if t["kind"] == "ref":
        return [t["name"]]
    return refs(t.get("element"))


def reachable(definitions: dict[str, dict[str, Any]]) -> list[str]:
    """The definitions a TransactionEnvelope can hold, in the order of xdr.json."""
    seen: set[str] = set()
    stack = ["TransactionEnvelope"]
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(name)
        d = definitions[name]
        for f in d.get("fields", []):
            stack += refs(f["type"])
        for arm in d.get("arms", []):
            stack += refs(arm.get("type"))
        if d["kind"] == "union":
            stack += refs(d["discriminant"]["type"])
        if d["kind"] == "typedef":
            stack += refs(d["type"])
    return [name for name in definitions if name in seen]


def python_name(xdr_name: str) -> str:
    """The name stellar_xdr exports a definition under.

    It capitalizes a typedef such as `uint32`, and writes an acronym in capitals, as
    in `LedgerKeyTTL`; the names differ in case only.
    """
    matches = [n for n in stellar_xdr.__all__ if n.lower() == xdr_name.lower()]
    if len(matches) != 1:
        sys.exit(f"stellar_xdr has no single class for {xdr_name}: {matches}")
    return matches[0]


def arm_classes(namespace: type) -> tuple[str, dict[int, tuple[str, str | None]]]:
    """The attribute of a union's discriminant, and its arms by their discriminant.

    Each arm is the name of its class and the attribute of its value, if any.
    """
    attributes: set[str] = set()
    arms: dict[int, tuple[str, str | None]] = {}
    classes = {
        cls
        for cls in vars(namespace).values()
        if isinstance(cls, type) and issubclass(cls, stellar_xdr.XdrArm)
    }
    for cls in classes:
        found = [
            (k, v)
            for k, v in vars(cls).items()
            if not k.startswith("_") and isinstance(v, int)
        ]
        if len(found) != 1 or getattr(namespace, cls.__name__) is not cls:
            sys.exit(f"{namespace.__name__}.{cls.__name__}: unexpected arm class")
        attribute, value = found[0]
        attributes.add(attribute)
        fields = cls.__match_args__
        arms[int(value)] = (cls.__name__, fields[0] if fields else None)
    if len(attributes) != 1:
        sys.exit(f"{namespace.__name__}: no single discriminant attribute")
    return attributes.pop(), arms


def entry(d: dict[str, Any]) -> tuple[Any, ...]:
    """The schema entry of one definition."""
    kind = d["kind"]
    if kind == "typedef":
        return ("typedef", type_of(d["type"]))
    name = python_name(d["name"])
    cls = getattr(stellar_xdr, name)
    if kind == "enum":
        return ("enum", name)
    if kind == "struct":
        attributes = cls.__match_args__
        if len(attributes) != len(d["fields"]):
            sys.exit(f"{name}: the fields of xdr.json and stellar_xdr differ")
        fields = tuple(
            (f["name"], attribute, type_of(f["type"]))
            for f, attribute in zip(d["fields"], attributes, strict=True)
        )
        return ("struct", name, fields)
    attribute, classes = arm_classes(cls)
    arms: dict[int, tuple[Any, ...]] = {}
    for arm in d["arms"]:
        held = None if arm.get("type") is None else type_of(arm["type"])
        for case in arm["cases"]:
            value = case["value"]
            if value not in classes or (held is None) != (classes[value][1] is None):
                sys.exit(f"{name}: no arm class for {value}")
            arm_class, field = classes[value]
            arms[value] = (arm_class, arm.get("name"), field, held)
    if set(arms) != set(classes):
        sys.exit(f"{name}: the arms of xdr.json and stellar_xdr differ")
    discriminant = d["discriminant"]
    return (
        "union",
        name,
        discriminant["name"],
        attribute,
        type_of(discriminant["type"]),
        arms,
    )


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    data = Path(sys.argv[1]).read_bytes()
    definitions = {d["name"]: d for d in json.loads(data)["definitions"]}
    schema = {name: entry(definitions[name]) for name in reachable(definitions)}
    source = f'''"""The XDR definitions of a transaction envelope, for txrep. Do not edit.

Written by scripts/txrep_schema.py from xdr.json (sha256 {hashlib.sha256(data).hexdigest()}).

Each definition is ("struct", class, ((field, attribute, type), ...)), ("union",
namespace, discriminant, its attribute, its type, {{value: (arm class, arm, attribute,
type)}}), ("enum", class) or ("typedef", type): the XDR names, and the names in
stellar_xdr. An arm without a value has None for its name, attribute and type. A type
is ("ref", definition), ("bool",), ("int",), ("uint",), ("hyper",), ("uhyper",),
("opaque", size), ("var_opaque", max size), ("string", max size), ("var_array", type,
max count) or ("optional", type); a max of None is no max.
"""

from typing import Any

SCHEMA: dict[str, tuple[Any, ...]] = {pprint.pformat(schema, width=88, sort_dicts=False)}
'''
    OUTPUT.write_text(source)
    print(f"wrote {len(schema)} definitions to {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
