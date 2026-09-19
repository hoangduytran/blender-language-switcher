#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0-or-later

"""Build the installable extension zip into ``dist/``.

Usage::

    python3 mk_install_zip.py                 # auto-detect Blender, else plain zip
    python3 mk_install_zip.py --blender PATH  # use a specific Blender executable
    python3 mk_install_zip.py --no-blender    # skip Blender, always use plain zip

When Blender (4.2+) is found, ``blender --command extension build`` is used and
the result is validated. Otherwise the zip is written directly with Python,
which gives the same layout: the add-on files at the root of the archive.

Blender is looked up in this order: ``--blender``, the ``BLENDER`` environment
variable, ``blender`` on ``PATH``, then ``/Applications/Blender*.app`` on macOS.
"""

from __future__ import annotations

import argparse
import fnmatch
import glob
import os
import re
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / "switch_language"
DIST_DIR = ROOT / "dist"
MANIFEST = SOURCE_DIR / "blender_manifest.toml"

# Mirrors `paths_exclude_pattern` in the manifest.
EXCLUDE_DIRS = {"__pycache__"}
EXCLUDE_NAME_PATTERNS = (".*", "*.pyc")


def read_manifest_field(name):
    match = re.search(
        r'^{}\s*=\s*"([^"]*)"'.format(re.escape(name)),
        MANIFEST.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    if match is None:
        sys.exit("error: '{}' not found in {}".format(name, MANIFEST))
    return match.group(1)


def find_blender(explicit):
    if explicit:
        return explicit
    if os.environ.get("BLENDER"):
        return os.environ["BLENDER"]
    on_path = shutil.which("blender")
    if on_path:
        return on_path
    if sys.platform == "darwin":
        # Newest-looking app bundle last, so take the final match.
        apps = sorted(glob.glob("/Applications/Blender*.app/Contents/MacOS/Blender"))
        if apps:
            return apps[-1]
    return None


def build_with_blender(blender, zip_path):
    print("Building with Blender:", blender)
    subprocess.run(
        [
            blender, "--factory-startup", "--command", "extension", "build",
            "--source-dir", str(SOURCE_DIR),
            "--output-filepath", str(zip_path),
        ],
        check=True,
    )
    subprocess.run(
        [blender, "--factory-startup", "--command", "extension", "validate", str(zip_path)],
        check=True,
    )


def is_excluded(name):
    return any(fnmatch.fnmatch(name, pattern) for pattern in EXCLUDE_NAME_PATTERNS)


def build_with_zipfile(zip_path):
    print("Building with Python zipfile (no Blender validation)")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for dirpath, dirnames, filenames in os.walk(SOURCE_DIR):
            dirnames[:] = sorted(
                d for d in dirnames if d not in EXCLUDE_DIRS and not is_excluded(d)
            )
            for filename in sorted(filenames):
                if is_excluded(filename):
                    continue
                path = Path(dirpath) / filename
                archive.write(path, path.relative_to(SOURCE_DIR).as_posix())


def main():
    parser = argparse.ArgumentParser(description="Build the installable extension zip into dist/.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--blender", help="path to the Blender executable")
    group.add_argument("--no-blender", action="store_true", help="build with plain zip only")
    args = parser.parse_args()

    zip_path = DIST_DIR / "{}-{}.zip".format(
        read_manifest_field("id"), read_manifest_field("version"),
    )
    DIST_DIR.mkdir(exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()

    blender = None if args.no_blender else find_blender(args.blender)
    if blender:
        build_with_blender(blender, zip_path)
    else:
        build_with_zipfile(zip_path)

    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
    print("Created {} ({} files: {})".format(
        zip_path.relative_to(ROOT), len(names), ", ".join(names),
    ))


if __name__ == "__main__":
    main()
