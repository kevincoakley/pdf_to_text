# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python tool for extracting high-quality text from academic PDF papers using the `unstructured` library. The tool is optimized specifically for academic papers and conference proceedings, using high-resolution extraction strategies to preserve document structure, tables, and formatting.

## Architecture

The project follows a simple, single-script architecture:

- **`extract_pdf_text.py`** - Main processing script that handles batch PDF extraction
- **Input**: PDFs placed in `pdf/` directory  
- **Output**: Text files in `results/` directory with clean, readable text organized by sections

## Key Dependencies

- **System dependency**: `poppler` (install via `brew install poppler`)
- **Python**: Requires 3.9+ for `unstructured` library compatibility
- **Package manager**: Uses `uv` for dependency management

## Common Commands

### Setup and Installation
```bash
# Install system dependency
brew install poppler

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
- **Strategy**: `hi_res` for maximum quality
- **Table structure**: Enabled to preserve academic tables
- **Image extraction**: Disabled (text-focused)
- **Chunking**: Title-based to maintain document hierarchy

## Output Structure

Each PDF generates a single text file with clean text and document structure preserved for LLM analysis. The text is organized by titles/sections to maintain document hierarchy.

## Error Handling

The tool continues processing even if individual PDFs fail, providing summary statistics at completion. Common failures relate to corrupted PDFs or unsupported formatting.

## Git Management
- Use gpg signing for commits: `git commit -S`
- Follow conventional commit messages for clarity
- Use `git pull --rebase` to keep history clean

