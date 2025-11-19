# PDF to Text Extractor

## Dependencies

This project uses the following key dependencies:

- **PyMuPDF** - High-performance PDF text extraction library
- **Python 3.9+** - Required for PyMuPDF compatibility

## Installation

Using the UV package manager (recommended):

```bash
# Install UV if you haven't already
pip install uv

# Install project dependencies
uv sync
```

## Usage

Run the extraction script on a single PDF file:

```bash
uv run extract_pdf_text.py <path_to_pdf>
```