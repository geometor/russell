"""Codex continuity, folio correlation, and archival plate tests for walter-russell."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCSRC = REPO_ROOT / "docsrc"
HSC_DIR = DOCSRC / "home_study_course"
COSMOGONY_DIR = DOCSRC / "cosmogony"
FOLIOS_DIR = REPO_ROOT / "resources" / "home_study_course" / "folios"


def test_all_519_folio_scans_exist() -> None:
    scans = sorted(p.name for p in FOLIOS_DIR.glob("*.png"))
    expected = [f"{i:04d}.png" for i in range(1, 520)]
    assert scans == expected


def test_home_study_course_100_percent_folio_coverage_and_monotonic() -> None:
    rst_files = sorted(HSC_DIR.rglob("*.rst"))
    assert len(rst_files) == 62  # index + prelude + 12 part indices + 48 lessons

    for rst_path in rst_files:
        text = rst_path.read_text(encoding="utf-8")
        assert re.search(r"^:folio:\s*\d{4}\s*$", text, re.MULTILINE), (
            f"Missing :folio: frontmatter badge in {rst_path.relative_to(REPO_ROOT)}"
        )
        assert re.search(r"^\.\.\s+folio::\s*\d{4}\s*$", text, re.MULTILINE), (
            f"Missing .. folio:: directive in {rst_path.relative_to(REPO_ROOT)}"
        )
        assert re.search(r"^\s+:page:\s*\d+\s*$", text, re.MULTILINE), (
            f"Missing :page: option on .. folio:: in {rst_path.relative_to(REPO_ROOT)}"
        )

    ordered_leaves = [HSC_DIR / "index.rst", HSC_DIR / "prelude.rst"] + sorted(
        HSC_DIR.glob("part_*/lesson_*.rst")
    )
    seen_folios: list[str] = []
    for leaf in ordered_leaves:
        seen_folios.extend(
            re.findall(r"^\.\.\s+folio::\s*(\d{4})\s*$", leaf.read_text(encoding="utf-8"), re.MULTILINE)
        )

    expected = [f"{i:04d}" for i in range(1, 520)]
    assert seen_folios == expected, "Folios 0001..0519 must appear in strict monotonic sequence without gaps"


def test_cosmogony_100_percent_folio_coverage() -> None:
    rst_files = sorted(COSMOGONY_DIR.rglob("*.rst"))
    assert len(rst_files) == 16

    for rst_path in rst_files:
        text = rst_path.read_text(encoding="utf-8")
        assert re.search(r"^:folio:\s*\d{4}\s*$", text, re.MULTILINE), (
            f"Missing :folio: frontmatter badge in {rst_path.relative_to(REPO_ROOT)}"
        )
        assert re.search(r"^\.\.\s+folio::\s*\d{4}\s*$", text, re.MULTILINE), (
            f"Missing .. folio:: directive in {rst_path.relative_to(REPO_ROOT)}"
        )
        assert re.search(r"^\s+:page:\s*\d+\s*$", text, re.MULTILINE), (
            f"Missing :page: option on .. folio:: in {rst_path.relative_to(REPO_ROOT)}"
        )


def test_legacy_anchors_and_concise_titles_preserved() -> None:
    assert ".. _hsc-prelude:" in (HSC_DIR / "prelude.rst").read_text(encoding="utf-8")
    for n in range(1, 49):
        lesson_paths = list(HSC_DIR.glob(f"part_*/lesson_{n:02d}.rst"))
        assert len(lesson_paths) == 1, f"Expected single leaf for Lesson {n}"
        text = lesson_paths[0].read_text(encoding="utf-8")
        assert f".. _hsc-lesson-{n:02d}:" in text
        m_h1 = re.search(r"^(Lesson \d+[^\n]+)\n=+\s*$", text, re.MULTILINE)
        assert m_h1 is not None
        assert not m_h1.group(1).startswith("LESSON NUMBER "), (
            f"Lesson {n} still uses unpolished ALL-CAPS title: {m_h1.group(1)}"
        )

    for ch in range(1, 8):
        ch_paths = list(COSMOGONY_DIR.glob(f"{ch:02d}_*.rst"))
        assert len(ch_paths) == 1
        assert f".. _cosmogony-ch{ch}:" in ch_paths[0].read_text(encoding="utf-8")


def test_all_33_chalkboard_plates_embedded_and_clean() -> None:
    g1_files = sorted(HSC_DIR.rglob("*.g1.png"))
    assert len(g1_files) == 33

    all_hsc_rst = "\n".join(p.read_text(encoding="utf-8") for p in HSC_DIR.rglob("*.rst"))
    for g1 in g1_files:
        assert f".. picture:: {g1.name}" in all_hsc_rst, f"Orphaned plate: {g1.relative_to(REPO_ROOT)}"

    # Ensure .. picture:: never uses :align: or :width:, and zero .. py_file:: directives exist
    for rst_path in DOCSRC.rglob("*.rst"):
        lines = rst_path.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            assert not line.strip().startswith(".. py_file::"), f"Forbidden .. py_file:: in {rst_path}"
            if line.strip().startswith(".. picture::"):
                j = i + 1
                while j < len(lines) and (not lines[j].strip() or lines[j].startswith((" ", "\t"))):
                    assert not re.match(r"^\s+:(?:align|width):", lines[j]), (
                        f"Forbidden :align:/:width: on .. picture:: in {rst_path}:{j + 1}"
                    )
                    j += 1
