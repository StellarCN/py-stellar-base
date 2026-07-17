"""Shared helpers for the test suite.

The utilities here serve two goals:

* **Determinism** — unit tests use :func:`deterministic_keypair` (or the
  well-known keypairs below) instead of ``Keypair.random()``, so signatures
  and XDR are reproducible across runs. Integration tests intentionally keep
  ``Keypair.random()``: friendbot refuses to re-fund an existing account.
* **One test body for sync and async** — :func:`resolve` and :func:`take`
  let a single ``async def`` test drive both the sync and async variants of
  an SDK API.
"""

import hashlib
from collections.abc import AsyncIterator, Awaitable, Iterator
from typing import TypeVar

from stellar_sdk import Keypair

T = TypeVar("T")


async def resolve(value: "T | Awaitable[T]") -> T:
    """Await *value* if it is awaitable, otherwise return it unchanged.

    Lets one async test body drive both sync and async servers::

        account = await resolve(server.load_account(account_id))
    """
    if isinstance(value, Awaitable):
        return await value
    return value


async def take(source: "Iterator[T] | AsyncIterator[T]", n: int) -> list[T]:
    """Collect the first *n* items from a sync or async iterator."""
    items: list[T] = []
    if isinstance(source, AsyncIterator):
        async for item in source:
            items.append(item)
            if len(items) == n:
                break
    else:
        for item in source:
            items.append(item)
            if len(items) == n:
                break
    return items


def deterministic_keypair(name: str) -> Keypair:
    """Return a distinct, reproducible keypair derived from *name*.

    Ed25519 signing is deterministic (RFC 8032), so tests built on these
    keypairs can assert exact signatures and XDR.
    """
    seed = hashlib.sha256(f"py-stellar-base:test:{name}".encode()).digest()
    return Keypair.from_raw_ed25519_seed(seed)


# Well-known cast used across tests instead of ad-hoc secret-seed literals.
SERVER_KP = deterministic_keypair("server")
CLIENT_KP = deterministic_keypair("client")
CLIENT_DOMAIN_KP = deterministic_keypair("client-domain")
SIGNER1_KP = deterministic_keypair("signer-1")
SIGNER2_KP = deterministic_keypair("signer-2")
SIGNER3_KP = deterministic_keypair("signer-3")
