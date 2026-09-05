#!/usr/bin/env python3
"""Validate the reusable structure and presentation exports of a concept pack."""

from __future__ import annotations

import argparse
import re
import struct
import zipfile
from pathlib import Path


REQUIRED_BRIEF_KEYS = (
    "idea_name",
    "idea",
    "audience",
    "question_to_provoke",
    "house_style",
)

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

# Supporting rasters are free-ratio; only composition pages must be 16:9.
SUPPORTING_DIR_PARTS = {"assets", "references"}

# Nested rerun directories are separate packs; check them only when invoked as the pack root.
NESTED_RERUN_DIR = "reruns"
SUPPORTING_NAME_PREFIXES = ("ink-layer", "asset-", "reference-", "contact-sheet-crop")

# Three-argument rotate(angle cx cy) is dropped by some SVG renderers.
UNSAFE_ROTATE = re.compile(r"rotate\(\s*-?[\d.]+\s*[, ]\s*-?[\d.]+\s*[, ]\s*-?[\d.]+\s*\)")

DRAFT_SUFFIX = re.compile(r"^(?P<stem>.+)-draft-(?P<n>\d+)$")


def pack_files(pack: Path, pattern: str) -> list[Path]:
    """Files matching *pattern* under *pack*, excluding anything inside a nested reruns/ directory."""
    return sorted(
        path
        for path in pack.rglob(pattern)
        if NESTED_RERUN_DIR not in path.relative_to(pack).parts[:-1]
    )


def png_size(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) != 24 or header[:8] != PNG_SIGNATURE:
        return None
    return struct.unpack(">II", header[16:24])


def is_supporting_raster(relative: Path) -> bool:
    if any(part in SUPPORTING_DIR_PARTS for part in relative.parts[:-1]):
        return True
    if "design-handoff" in relative.parts and "assets" in relative.parts:
        return True
    return relative.name.startswith(SUPPORTING_NAME_PREFIXES)


def check_drafts(pack: Path, errors: list[str]) -> None:
    """Every -draft-N (N >= 2) must sit beside its predecessor's editable source."""
    for source in pack_files(pack, "*.svg") + pack_files(pack, "*.html"):
        match = DRAFT_SUFFIX.match(source.stem)
        if not match:
            continue
        number = int(match.group("n"))
        if number < 2:
            continue
        stem = match.group("stem")
        candidates = [source.with_name(f"{stem}-draft-{number - 1}{source.suffix}")]
        if number == 2:
            candidates.append(source.with_name(f"{stem}{source.suffix}"))
        if not any(candidate.is_file() for candidate in candidates):
            names = " or ".join(candidate.name for candidate in candidates)
            errors.append(
                f"{source.relative_to(pack)} exists but its previous draft ({names}) is missing; "
                "earlier drafts must be preserved when the draft number increases"
            )


def check_pptx_fallbacks(pack: Path, errors: list[str]) -> None:
    """Any .png stored in a PPTX must really be a PNG, not SVG bytes."""
    for deck in pack_files(pack, "*.pptx"):
        try:
            with zipfile.ZipFile(deck) as archive:
                for name in archive.namelist():
                    if not name.lower().startswith("ppt/media/") or not name.lower().endswith(".png"):
                        continue
                    head = archive.open(name).read(8)
                    if head != PNG_SIGNATURE:
                        errors.append(
                            f"{deck.relative_to(pack)} embeds {name} that is not a genuine PNG "
                            "(likely SVG bytes under a .png name); replace the raster fallback"
                        )
        except zipfile.BadZipFile:
            errors.append(f"invalid PPTX archive: {deck.relative_to(pack)}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a product-idea pack.")
    parser.add_argument("pack", type=Path, help="Pack directory")
    args = parser.parse_args()
    pack = args.pack.resolve()

    errors: list[str] = []
    warnings: list[str] = []
    if not pack.is_dir():
        parser.error(f"pack directory not found: {pack}")

    brief_path = pack / "brief.yaml"
    if not brief_path.is_file():
        errors.append("missing brief.yaml")
    else:
        brief = brief_path.read_text(encoding="utf-8")
        for key in REQUIRED_BRIEF_KEYS:
            if not re.search(rf"(?m)^{re.escape(key)}\s*:", brief):
                errors.append(f"brief.yaml is missing key: {key}")
        if re.search(r"(?mi)^\s*private_test_material_included\s*:\s*true\s*$", brief):
            errors.append("brief.yaml marks private test material as included")

    pngs = pack_files(pack, "*.png")
    if not pngs:
        warnings.append("no PNG presentation exports found")
    for image in pngs:
        dimensions = png_size(image)
        relative = image.relative_to(pack)
        if dimensions is None:
            errors.append(f"invalid PNG header: {relative}")
            continue
        width, height = dimensions
        if is_supporting_raster(relative):
            continue
        is_prototype_capture = any("prototype" in part for part in relative.parts)
        if is_prototype_capture:
            if width < 320 or height < 320:
                warnings.append(f"small prototype PNG {relative}: {width}x{height}")
        else:
            ratio = width / height
            if abs(ratio - (16 / 9)) > 0.02:
                warnings.append(f"non-16:9 presentation PNG {relative}: {width}x{height}")
            if width < 1200 or height < 675:
                warnings.append(f"small presentation PNG {relative}: {width}x{height}")

    for svg in pack_files(pack, "*.svg"):
        if UNSAFE_ROTATE.search(svg.read_text(encoding="utf-8", errors="replace")):
            warnings.append(
                f"{svg.relative_to(pack)} uses rotate(angle cx cy), which some renderers drop; "
                "use translate/rotate instead"
            )

    for prototype in pack_files(pack, "*.html"):
        html = prototype.read_text(encoding="utf-8")
        if "prototype" in prototype.name.lower() or any(
            "prototype" in part for part in prototype.parts
        ):
            if "data-prototype-root" not in html:
                warnings.append(
                    f"prototype lacks data-prototype-root: {prototype.relative_to(pack)}"
                )
            if "data-stage-button" not in html:
                warnings.append(
                    f"prototype lacks exportable stages: {prototype.relative_to(pack)}"
                )

    check_drafts(pack, errors)
    check_pptx_fallbacks(pack, errors)

    for message in warnings:
        print(f"WARNING: {message}")
    for message in errors:
        print(f"ERROR: {message}")

    if errors:
        print(f"Pack check failed with {len(errors)} error(s).")
        return 1
    print(f"Pack check passed with {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
