"""Tests for PDF text extraction script."""

from __future__ import annotations

from pathlib import Path

import pytest

import extract_pdf_text

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def sample_paths() -> tuple[Path, Path]:
    """Return sample PDF and expected TXT directories."""
    return PROJECT_ROOT / "examples" / "pdf", PROJECT_ROOT / "examples" / "txt"


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    """Return a temporary output directory."""
    return tmp_path / "generated_txt"


def test_parse_args_uses_custom_paths() -> None:
    """CLI parser should accept --pdf-path and --txt-path values."""
    args = extract_pdf_text.parse_args(["--pdf-path", "in", "--txt-path", "out"])

    assert args.pdf_path == Path("in")
    assert args.txt_path == Path("out")


def test_clean_non_latin_chars_removes_unsupported_symbols() -> None:
    """Unsupported symbols should be removed while preserving useful text."""
    cleaned = extract_pdf_text.clean_non_latin_chars("Alpha β test @email.com ✓")

    assert cleaned == "Alpha β test @email.com"


def test_process_pdf_directory_raises_for_missing_path(tmp_path: Path) -> None:
    """Missing PDF directories should raise a clear error."""
    missing_dir = tmp_path / "does-not-exist"

    with pytest.raises(FileNotFoundError):
        extract_pdf_text.process_pdf_directory(missing_dir, tmp_path / "out")


def test_examples_match_expected_output(
    sample_paths: tuple[Path, Path], output_dir: Path
) -> None:
    """Generated TXT output should match expected files for the example PDFs."""
    pdf_dir, expected_txt_dir = sample_paths

    success_count, error_count = extract_pdf_text.process_pdf_directory(
        pdf_dir, output_dir
    )

    expected_files = sorted(expected_txt_dir.glob("*.txt"))
    generated_files = sorted(output_dir.glob("*.txt"))

    assert error_count == 0
    assert success_count == len(expected_files)
    assert [path.name for path in generated_files] == [
        path.name for path in expected_files
    ]

    for expected_file in expected_files:
        generated_file = output_dir / expected_file.name
        assert generated_file.exists()
        assert generated_file.read_text(encoding="utf-8") == expected_file.read_text(
            encoding="utf-8"
        )
