#!/usr/bin/env python3
"""Verify Python XDR-JSON (SEP-0051) output against the Rust stellar CLI.

For each transaction envelope in a CSV file, this script:
  1. Decodes via the Rust `stellar` CLI and the Python SDK
  2. Deep-compares the two JSON representations
  3. Verifies Python JSON round-trip (JSON -> object -> XDR == original XDR)

Usage:
    python verify_xdr_json.py transactions.csv
    python verify_xdr_json.py transactions.csv --column tx_envelope --limit 5000
    python verify_xdr_json.py transactions.csv --verbose
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from stellar_sdk.xdr import FeeBumpTransactionEnvelope, TransactionEnvelope

XDR_TYPES = ["TransactionEnvelope", "FeeBumpTransactionEnvelope"]

PYTHON_DECODERS = {
    "TransactionEnvelope": (
        TransactionEnvelope.from_xdr,
        TransactionEnvelope.from_json_dict,
    ),
    "FeeBumpTransactionEnvelope": (
        FeeBumpTransactionEnvelope.from_xdr,
        FeeBumpTransactionEnvelope.from_json_dict,
    ),
}


@dataclass
class Stats:
    total: int = 0
    rust_errors: int = 0
    python_errors: int = 0
    json_matched: int = 0
    json_mismatched: int = 0
    roundtrip_ok: int = 0
    roundtrip_fail: int = 0
    first_mismatches: list[str] = field(default_factory=list)
    first_roundtrip_failures: list[str] = field(default_factory=list)

    MAX_SAMPLES = 10

    def record_mismatch(self, row_num: int, diffs: list[str]) -> None:
        self.json_mismatched += 1
        if len(self.first_mismatches) < self.MAX_SAMPLES:
            detail = "\n".join(diffs[:5])
            self.first_mismatches.append(f"[row {row_num}]\n{detail}")

    def record_roundtrip_failure(self, row_num: int, reason: str) -> None:
        self.roundtrip_fail += 1
        if len(self.first_roundtrip_failures) < self.MAX_SAMPLES:
            self.first_roundtrip_failures.append(f"[row {row_num}] {reason}")


def rust_decode(xdr_b64: str) -> tuple[dict | None, str | None]:
    """Decode XDR base64 using the Rust ``stellar`` CLI."""
    for xdr_type in XDR_TYPES:
        result = subprocess.run(
            ["stellar", "xdr", "decode", "--type", xdr_type, xdr_b64],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return json.loads(result.stdout), xdr_type
    return None, None


def python_decode(xdr_b64: str) -> tuple[dict | None, str | None, Any]:
    """Decode XDR base64 using the Python SDK."""
    for xdr_type, (from_xdr, _) in PYTHON_DECODERS.items():
        try:
            obj = from_xdr(xdr_b64)
            return obj.to_json_dict(), xdr_type, obj
        except Exception:
            continue
    return None, None, None


def deep_compare(
    rust_val: Any,
    python_val: Any,
    path: str = "$",
) -> list[str]:
    """Recursively compare two JSON-like structures, returning human-readable diffs."""
    diffs: list[str] = []

    if type(rust_val) is not type(python_val):
        diffs.append(
            f"{path}: type mismatch — "
            f"rust={type(rust_val).__name__}({rust_val!r})  "
            f"python={type(python_val).__name__}({python_val!r})"
        )
        return diffs

    if isinstance(rust_val, dict):
        all_keys = sorted(set(rust_val) | set(python_val))
        for key in all_keys:
            child_path = f"{path}.{key}"
            if key not in rust_val:
                diffs.append(f"{child_path}: missing in rust")
            elif key not in python_val:
                diffs.append(f"{child_path}: missing in python")
            else:
                diffs.extend(deep_compare(rust_val[key], python_val[key], child_path))
    elif isinstance(rust_val, list):
        if len(rust_val) != len(python_val):
            diffs.append(
                f"{path}: array length — rust={len(rust_val)} vs python={len(python_val)}"
            )
        for i in range(min(len(rust_val), len(python_val))):
            diffs.extend(deep_compare(rust_val[i], python_val[i], f"{path}[{i}]"))
    elif rust_val != python_val:
        diffs.append(f"{path}: {rust_val!r} (rust) != {python_val!r} (python)")

    return diffs


def verify_roundtrip(
    python_json: dict,
    python_type: str,
    original_xdr: str,
) -> str | None:
    """Round-trip: JSON dict -> Python object -> XDR base64. Returns error message or None."""
    _, from_json_dict = PYTHON_DECODERS[python_type]
    try:
        obj2 = from_json_dict(python_json)
    except Exception as exc:
        return f"from_json_dict failed: {exc}"

    try:
        xdr2 = obj2.to_xdr()
    except Exception as exc:
        return f"to_xdr failed: {exc}"

    if xdr2 != original_xdr:
        return "XDR mismatch after round-trip"
    return None


def process_csv(
    csv_path: Path,
    column: str,
    limit: int,
    verbose: bool,
    progress_interval: int,
) -> Stats:
    stats = Stats()
    t0 = time.monotonic()

    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        if column not in (reader.fieldnames or []):
            print(f"Error: column '{column}' not found in CSV.", file=sys.stderr)
            print(f"Available columns: {reader.fieldnames}", file=sys.stderr)
            sys.exit(1)

        for i, row in enumerate(reader):
            if i >= limit:
                break

            xdr_b64 = row[column].strip()
            if not xdr_b64:
                continue
            stats.total += 1
            row_num = i + 1

            # --- Rust decode ---
            rust_json, rust_type = rust_decode(xdr_b64)
            if rust_json is None:
                stats.rust_errors += 1
                if verbose:
                    print(f"[row {row_num}] WARN: Rust decode failed", file=sys.stderr)
                continue

            # --- Python decode ---
            python_json, python_type, _ = python_decode(xdr_b64)
            if python_json is None or python_type is None:
                stats.python_errors += 1
                if verbose:
                    print(
                        f"[row {row_num}] ERROR: Python decode failed", file=sys.stderr
                    )
                continue

            # --- Compare JSON ---
            diffs = deep_compare(rust_json, python_json)
            if diffs:
                stats.record_mismatch(row_num, diffs)
                if verbose:
                    print(f"[row {row_num}] JSON MISMATCH ({len(diffs)} diff(s))")
            else:
                stats.json_matched += 1

            # --- Round-trip ---
            err = verify_roundtrip(python_json, python_type, xdr_b64)
            if err is None:
                stats.roundtrip_ok += 1
            else:
                stats.record_roundtrip_failure(row_num, err)
                if verbose:
                    print(f"[row {row_num}] ROUND-TRIP FAIL: {err}")

            # --- Progress ---
            if progress_interval and stats.total % progress_interval == 0:
                elapsed = time.monotonic() - t0
                rate = stats.total / elapsed if elapsed > 0 else 0
                print(
                    f"  ... {stats.total} processed ({rate:.0f} tx/s)",
                    file=sys.stderr,
                )

    return stats


def print_report(stats: Stats, elapsed: float) -> None:
    w = 60
    print(f"\n{'=' * w}")
    print(f"  Total transactions:   {stats.total:>8}")
    print(f"  Rust decode errors:   {stats.rust_errors:>8}")
    print(f"  Python decode errors: {stats.python_errors:>8}")
    print(f"{'─' * w}")
    print(f"  JSON matched:         {stats.json_matched:>8}")
    print(f"  JSON mismatched:      {stats.json_mismatched:>8}")
    print(f"{'─' * w}")
    print(f"  Round-trip OK:        {stats.roundtrip_ok:>8}")
    print(f"  Round-trip FAIL:      {stats.roundtrip_fail:>8}")
    print(f"{'─' * w}")
    print(f"  Elapsed:              {elapsed:>7.1f}s")
    print(f"{'=' * w}")

    if stats.first_mismatches:
        print(f"\nFirst {len(stats.first_mismatches)} JSON mismatch(es):")
        for sample in stats.first_mismatches:
            print(sample)
            print()

    if stats.first_roundtrip_failures:
        print(f"First {len(stats.first_roundtrip_failures)} round-trip failure(s):")
        for sample in stats.first_roundtrip_failures:
            print(sample)

    # Exit code
    if stats.json_mismatched or stats.roundtrip_fail or stats.python_errors:
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify Python XDR-JSON output against the Rust stellar CLI.",
    )
    parser.add_argument(
        "csv_file",
        type=Path,
        help="Path to CSV file containing XDR-encoded transaction envelopes.",
    )
    parser.add_argument(
        "--column",
        default="tx_envelope",
        help="CSV column name containing XDR base64 data (default: tx_envelope).",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Maximum number of rows to process (default: 0 = unlimited).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print each mismatch/failure as it occurs.",
    )
    parser.add_argument(
        "--progress",
        type=int,
        default=2000,
        help="Print progress every N transactions (default: 2000, 0 = off).",
    )
    args = parser.parse_args()

    if not args.csv_file.is_file():
        print(f"Error: file not found: {args.csv_file}", file=sys.stderr)
        sys.exit(1)

    limit = args.limit if args.limit > 0 else sys.maxsize

    t0 = time.monotonic()
    stats = process_csv(args.csv_file, args.column, limit, args.verbose, args.progress)
    elapsed = time.monotonic() - t0

    print_report(stats, elapsed)


if __name__ == "__main__":
    main()
