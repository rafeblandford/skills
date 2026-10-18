#!/usr/bin/env python3
"""Create a share archive from an explicit list of approved files."""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a zip from explicitly selected shareable files."
    )
    parser.add_argument("output", type=Path, help="Destination .zip path")
    parser.add_argument("files", nargs="+", type=Path, help="Files to include")
    parser.add_argument(
        "--base",
        type=Path,
        help="Optional base directory; preserve each input path relative to it",
    )
    args = parser.parse_args()

    output = args.output.resolve()
    if output.suffix.lower() != ".zip":
        parser.error("output must end in .zip")

    inputs = [item.resolve() for item in args.files]
    base = args.base.resolve() if args.base else None
    missing = [str(item) for item in inputs if not item.is_file()]
    if missing:
        parser.error("missing input files: " + ", ".join(missing))

    suspicious = [str(item) for item in inputs if "private-test" in str(item).lower()]
    if suspicious:
        parser.error("private test material cannot enter a share pack: " + ", ".join(suspicious))

    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", ZIP_DEFLATED) as archive:
        used_names: set[str] = set()
        for item in inputs:
            if base:
                try:
                    arcname = item.relative_to(base)
                except ValueError:
                    parser.error(f"input is outside --base: {item}")
            else:
                arcname = Path(item.name)
            archive_name = arcname.as_posix()
            if archive_name in used_names:
                parser.error(f"duplicate archive filename: {archive_name}")
            used_names.add(archive_name)
            archive.write(item, arcname=archive_name)

    print(f"Created {output} with {len(inputs)} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
