#!/usr/bin/env python3
"""Extract and clean text from every PDF in a directory."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, Sequence

import fitz

NON_LATIN_RE = re.compile(r"[^\w\s.,;:!?()[\]{}\"'\-@#/\\._+\-*=%<>&$|~]")
MULTI_WHITESPACE_RE = re.compile(r"\s+")


def clean_non_latin_chars(text: str) -> str:
    """Remove characters outside the accepted Latin/punctuation set."""
    cleaned = NON_LATIN_RE.sub(" ", text)
    cleaned = MULTI_WHITESPACE_RE.sub(" ", cleaned)
    return cleaned.strip()


def clean_text(text: str) -> str:
    """Normalize extracted text to reduce common PDF parsing artifacts."""
    substitutions: list[tuple[str, str]] = [
        (r"(\w)-\s+(\w)", r"\1\2"),
        (r"(\w)-\s*\n\s*(\w)", r"\1\2"),
        (r"(\w)-\n(\w)", r"\1\2"),
        (r"\n\s*\d+\s*$", ""),
        (r"\n\s*[\d\-–—]+\s*$", ""),
        (r"([a-z])([A-Z])", r"\1 \2"),
        (r"\s+", " "),
        (r"\n\s*•\s*", "\n• "),
        (r"\n\s*(\d+\.)\s*", r"\n\1 "),
        (r"\s{2,}", " "),
    ]

    for pattern, replacement in substitutions:
        text = re.sub(pattern, replacement, text)

    return text.strip()


def extract_text_blocks(doc: fitz.Document) -> list[str]:
    """Extract cleaned text blocks from a PyMuPDF document."""
    text_blocks: list[str] = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")

        for block in blocks.get("blocks", []):
            if "lines" not in block:
                continue

            line_segments: list[str] = []
            for line in block["lines"]:
                spans = line.get("spans", [])
                line_segments.append("".join(span.get("text", "") for span in spans))

            raw_block = " ".join(line_segments).strip()
            if not raw_block:
                continue

            cleaned_block = clean_non_latin_chars(raw_block)
            if cleaned_block and len(cleaned_block) > 3:
                text_blocks.append(cleaned_block)

    return text_blocks


def write_text_output(
    pdf_path: Path, output_dir: Path, text_blocks: Iterable[str]
) -> Path:
    """Write the extracted text blocks into one TXT file for a PDF."""
    output_file = output_dir / f"{pdf_path.stem}.txt"

    with output_file.open("w", encoding="utf-8") as file_handle:
        file_handle.write(f"# {pdf_path.name}\n\n")
        for block in text_blocks:
            cleaned_block = clean_text(block)
            if cleaned_block and len(cleaned_block) > 10:
                file_handle.write(f"{cleaned_block}\n\n")

    return output_file


def process_pdf(pdf_path: Path, output_dir: Path) -> Path:
    """Extract and write text for one PDF file."""
    print(f"Processing: {pdf_path.name}")

    with fitz.open(str(pdf_path)) as document:
        text_blocks = extract_text_blocks(document)

    output_file = write_text_output(pdf_path, output_dir, text_blocks)
    print(f"Completed: {pdf_path.name} -> {output_file.name}")
    return output_file


def get_pdf_files(pdf_dir: Path) -> list[Path]:
    """Return all PDF files in sorted order from a directory."""
    return sorted(pdf_dir.glob("*.pdf"))


def process_pdf_directory(pdf_dir: Path, output_dir: Path) -> tuple[int, int]:
    """Process all PDFs from ``pdf_dir`` and write TXTs under ``output_dir``."""
    if not pdf_dir.exists():
        raise FileNotFoundError(f"{pdf_dir} directory does not exist")
    if not pdf_dir.is_dir():
        raise NotADirectoryError(f"{pdf_dir} is not a directory")

    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_files = get_pdf_files(pdf_dir)

    if not pdf_files:
        print(f"No PDF files found in {pdf_dir}")
        return 0, 0

    print(f"Found {len(pdf_files)} PDF files to process")
    print(f"Output will be saved to: {output_dir.resolve()}")
    print("-" * 60)

    success_count = 0
    error_count = 0

    for pdf_file in pdf_files:
        try:
            process_pdf(pdf_file, output_dir)
            success_count += 1
        except Exception as exc:  # pragma: no cover - defensive logging branch
            print(f"Failed to process {pdf_file.name}: {exc}")
            error_count += 1

    print("-" * 60)
    print(f"Processing complete. Results saved in {output_dir.resolve()}")
    print(f"Successfully processed: {success_count} files")
    print(f"Failed to process: {error_count} files")

    return success_count, error_count


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments for input/output directories."""
    parser = argparse.ArgumentParser(
        description="Extract text from PDFs in a directory"
    )
    parser.add_argument(
        "--pdf-path",
        type=Path,
        default=Path("pdf"),
        help="Directory containing PDF files (default: ./pdf)",
    )
    parser.add_argument(
        "--txt-path",
        type=Path,
        default=Path("results"),
        help="Directory where TXT files will be written (default: ./results)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Run directory extraction from parsed command-line arguments."""
    args = parse_args(argv)

    try:
        _, error_count = process_pdf_directory(args.pdf_path, args.txt_path)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(f"Error: {exc}")
        return 1

    return 1 if error_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
