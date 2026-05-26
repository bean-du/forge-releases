#!/usr/bin/env python3
"""Generate latest.json for the Tauri updater feed.

Reads built bundles + minisign .sig files from a bundles directory and emits a
Tauri-compatible latest.json. Schema reference:
https://tauri.app/v1/guides/distribution/updater#dynamic-update-server

Usage:
    python3 gen-latest-json.py \\
      --version v0.6.0 \\
      --bundles-dir bundles \\
      --output latest.json
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

# Map (target triple, bundle suffix) -> Tauri platform key
PLATFORM_MAP: dict[str, list[tuple[str, str]]] = {
    "darwin-aarch64": [("aarch64-apple-darwin", ".dmg"), ("aarch64-apple-darwin", ".app.tar.gz")],
    "darwin-x86_64": [("x86_64-apple-darwin", ".dmg"), ("x86_64-apple-darwin", ".app.tar.gz")],
    "linux-x86_64": [("x86_64-unknown-linux-gnu", ".AppImage"), ("x86_64-unknown-linux-gnu", ".AppImage.tar.gz")],
    "windows-x86_64": [("x86_64-pc-windows-msvc", "-setup.exe"), ("x86_64-pc-windows-msvc", "-setup.nsis.zip")],
}


def find_bundle(bundles_dir: Path, target: str, suffix: str) -> Path | None:
    base = bundles_dir / target
    if not base.exists():
        return None
    matches = sorted(base.rglob(f"*{suffix}"))
    # Exclude .sig sidecars matched by glob
    matches = [m for m in matches if not m.name.endswith(".sig")]
    return matches[0] if matches else None


def read_signature(bundle: Path) -> str | None:
    sig_path = bundle.with_suffix(bundle.suffix + ".sig")
    if sig_path.exists():
        return sig_path.read_text().strip()
    return None


def build_release_url(repo: str, version: str, asset_name: str) -> str:
    return f"https://github.com/{repo}/releases/download/{version}/{asset_name}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Version tag, e.g. v0.6.0")
    parser.add_argument("--bundles-dir", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--repo",
        default="Aruakl/forge-releases",
        help="GitHub repo slug hosting the release",
    )
    parser.add_argument("--notes", default="See CHANGELOG.md for details.")
    args = parser.parse_args()

    if not args.bundles_dir.exists():
        print(f"error: bundles dir not found: {args.bundles_dir}", file=sys.stderr)
        return 2

    platforms: dict[str, dict[str, str]] = {}

    for platform_key, candidates in PLATFORM_MAP.items():
        # Prefer the updater-compatible archive (.app.tar.gz / .AppImage.tar.gz / -setup.nsis.zip)
        # because Tauri updater consumes archive + .sig, not the installer.
        chosen: Path | None = None
        for target, suffix in candidates:
            bundle = find_bundle(args.bundles_dir, target, suffix)
            if bundle and (".tar.gz" in suffix or ".nsis.zip" in suffix):
                chosen = bundle
                break
        if chosen is None:
            # Fallback: use the first found of any candidate
            for target, suffix in candidates:
                bundle = find_bundle(args.bundles_dir, target, suffix)
                if bundle:
                    chosen = bundle
                    break
        if chosen is None:
            print(f"warn: no bundle found for {platform_key}", file=sys.stderr)
            continue

        signature = read_signature(chosen)
        if signature is None:
            print(
                f"warn: no .sig sidecar for {chosen.name} — updater will reject this platform",
                file=sys.stderr,
            )
            signature = ""

        platforms[platform_key] = {
            "signature": signature,
            "url": build_release_url(args.repo, args.version, chosen.name),
        }

    if not platforms:
        print("error: no platforms found in bundles dir", file=sys.stderr)
        return 1

    payload = {
        "version": args.version,
        "notes": args.notes,
        "pub_date": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "platforms": platforms,
    }

    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(f"✓ Wrote {args.output} with {len(platforms)} platform(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
