# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python tool for extracting high-quality text from academic PDF papers using the `PyMuPDF` (fitz) library. The tool is optimized specifically for academic papers and conference proceedings, using block-based text extraction to preserve document structure and formatting while removing non-Latin characters and symbols.

## Architecture

The project follows a simple, single-script architecture:

- **`extract_pdf_text.py`** - Main processing script that handles batch PDF extraction
- **Input**: PDFs placed in `pdf/` directory  
- **Output**: Text files in `results/` directory with clean, readable text organized by sections

## Key Dependencies

- **PyMuPDF**: Core PDF text extraction library
- **Python**: Requires 3.9+ for PyMuPDF compatibility
- **Package manager**: Uses `uv` for dependency management

## Common Commands

### Setup and Installation
```bash
# Install Python dependencies
uv sync
```

### Running the Tool
```bash
# Process all PDFs in pdf/ directory
uv run python extract_pdf_text.py
```

### Adding Dependencies
```bash
# Add new dependency
uv add package_name
```

## Extraction Configuration

The tool is configured for academic papers with these settings:
- **Block-based extraction**: Uses PyMuPDF's text block structure for better organization
- **Character filtering**: Removes non-Latin characters and symbols while preserving letters, numbers, and punctuation
- **Text cleaning**: Fixes common PDF extraction issues like hyphenation and spacing
- **LLM-optimized**: Output is optimized for LLM analysis and processing

## Output Structure

Each PDF generates a single text file with clean text and document structure preserved for LLM analysis. The text is organized by titles/sections to maintain document hierarchy.

## Error Handling

The tool continues processing even if individual PDFs fail, providing summary statistics at completion. Common failures relate to corrupted PDFs or unsupported formatting.

## Git Management
- Use gpg signing for commits: `git commit -S`
- Follow conventional commit messages for clarity
- Use `git pull --rebase` to keep history clean

