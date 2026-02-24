# PDF to Text Extractor

## Setup

```bash
uv sync
```

## Run Extraction

```bash
uv run python extract_pdf_text.py --pdf-path examples/pdf --txt-path /tmp/pdf_txt_output
```

## Run Tests

```bash
uv sync --group test
uv run pytest
```

The test suite runs the extractor against `examples/pdf` and compares generated files to `examples/txt`.
