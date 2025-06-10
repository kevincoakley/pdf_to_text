# PDF to Text Extractor

A high-quality Python tool for extracting structured text from academic PDF papers using the `unstructured` library. Optimized for academic papers with advanced text processing capabilities including section detection, table structure preservation, and coordinate tracking.

## Features

- **High-Quality Text Extraction**: Uses `hi_res` strategy for maximum accuracy on academic papers
- **Clean Text Output**: Generates TXT files with structured, readable text
- **Table Structure Preservation**: Maintains table formatting and structure
- **Section/Heading Detection**: Automatically identifies and preserves document structure
- **Coordinate Tracking**: Includes precise text positioning information
- **Batch Processing**: Processes all PDFs in the `pdf/` directory automatically
- **Robust Error Handling**: Continues processing even if individual files fail
- **Academic Paper Optimized**: Specifically tuned for conference papers and academic documents

## Dependencies

This project uses the following key dependencies:

- **unstructured[pdf]** - Advanced PDF text extraction library
- **pillow** - Image processing support
- **pdfminer.six** - PDF parsing capabilities  
- **python-magic** - File type detection
- **pdf2image** - PDF to image conversion
- **poppler** - System dependency for PDF processing (installed via Homebrew)

## System Requirements

- **Python**: 3.9 or higher
- **macOS**: Homebrew for installing system dependencies
- **poppler**: Required system library for PDF processing

## Installation

### 1. Install System Dependencies

First, install poppler using Homebrew:

```bash
brew install poppler
```

### 2. Install Python Dependencies

Using the UV package manager (recommended):

```bash
# Install UV if you haven't already
pip install uv

# Install project dependencies
uv sync
```

Alternatively, using pip:

```bash
pip install -e .
```

## Usage

### Basic Usage

1. **Place PDF files** in the `pdf/` directory
2. **Run the extraction script**:

```bash
uv run python extract_pdf_text.py
```

### Output

The script processes all PDF files in the `pdf/` directory and saves results to the `results/` directory. For each PDF file, one output file is generated:

- **`filename.txt`** - Clean text output organized by document sections

### Example Output Structure

**TXT Output** provides clean, readable text:
```
# paper.pdf

Research Paper Title

Authors: John Doe, Jane Smith

Abstract
This paper presents...

Introduction
The field of research...
```

## Configuration

The extraction is configured for high-quality academic paper processing with these settings:

- **Strategy**: `hi_res` - Highest quality extraction
- **Table Structure**: Enabled - Preserves table formatting
- **Image Extraction**: Disabled - Focuses on text content
- **Page Breaks**: Included - Maintains document structure

## Performance

- **Processing Speed**: ~2-3 minutes per PDF (varies by complexity)
- **Quality**: Optimized for academic papers with complex formatting
- **Memory Usage**: Moderate - suitable for batch processing
- **Error Handling**: Robust - continues processing if individual files fail

## Troubleshooting

### Common Issues

1. **"Unable to get page count. Is poppler installed?"**
   ```bash
   brew install poppler
   ```

2. **Import errors with unstructured**
   ```bash
   uv sync  # Reinstall dependencies
   ```

3. **Memory issues with large PDFs**
   - Process PDFs in smaller batches
   - Consider using `fast` strategy for very large files

### Logs and Output

The script provides real-time progress updates:
```
Found 400 PDF files to process
Output will be saved to: /path/to/results
------------------------------------------------------------
Processing: paper1.pdf
✓ Completed: paper1.pdf -> paper1.txt
Processing: paper2.pdf
✓ Completed: paper2.pdf -> paper2.txt
------------------------------------------------------------
Processing complete! Results saved in /path/to/results
Successfully processed: 398 files
Failed to process: 2 files
```

## Directory Structure

```
pdf_to_text/
├── README.md
├── pyproject.toml          # UV package configuration
├── extract_pdf_text.py     # Main extraction script
├── pdf/                    # Input PDF files
│   ├── paper1.pdf
│   ├── paper2.pdf
│   └── ...
└── results/                # Output directory
    ├── paper1.txt          # Clean text output
    ├── paper2.txt          # Clean text output
    └── ...
```

## License

This project is open source and available under the MIT License.