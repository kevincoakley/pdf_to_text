import argparse
import sys
from pathlib import Path
import fitz  # PyMuPDF
import re


def clean_non_latin_chars(text: str) -> str:
    """Remove non-Latin characters and symbols while preserving letters, numbers, punctuation, and useful symbols."""
    # Keep Latin letters, numbers, standard punctuation, and useful symbols:
    # - Email/web: @ # / \ . _
    # - Math: + - * = % < >
    # - Other useful: & $ | ~
    cleaned = re.sub(r'[^\w\s.,;:!?()[\]{}"\'-@#/\\._+\-*=%<>&$|~]', " ", text)

    # Clean up multiple spaces created by character removal
    cleaned = re.sub(r"\s+", " ", cleaned)

    return cleaned.strip()


def clean_text(text: str) -> str:
    """Clean and fix common PDF extraction issues in academic papers."""
    # Enhanced hyphen handling for academic papers
    text = re.sub(r"(\w)-\s+(\w)", r"\1\2", text)  # Fix "word- word" -> "wordword"
    text = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)  # Fix hyphenated across lines
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)  # Handle line break hyphens

    # Remove common footer patterns
    text = re.sub(r"\n\s*\d+\s*$", "", text)  # Remove trailing page numbers
    text = re.sub(r"\n\s*[\d\-–—]+\s*$", "", text)  # Remove footer separators

    # Fix common PDF extraction issues
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)  # Fix merged words like "wordWord"
    text = re.sub(r"\s+", " ", text)  # Normalize whitespace (after hyphen fixes)

    # Preserve academic formatting
    text = re.sub(r"\n\s*•\s*", "\n• ", text)  # Fix bullet points
    text = re.sub(r"\n\s*(\d+\.)\s*", r"\n\1 ", text)  # Fix numbered lists

    # Clean up multiple spaces
    text = re.sub(r"\s{2,}", " ", text)  # Multiple spaces to single space

    return text.strip()


def extract_text_blocks(doc):
    """Extract text blocks from PDF document, filtering and cleaning as needed."""
    text_blocks = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        # Get text blocks with positioning info
        blocks = page.get_text("dict")

        for block in blocks["blocks"]:
            if "lines" in block:  # Text block
                block_text = ""
                for line in block["lines"]:
                    line_text = ""
                    for span in line["spans"]:
                        line_text += span["text"]
                    block_text += line_text + " "

                # Clean the block text
                block_text = block_text.strip()
                if block_text:
                    # Apply character cleaning
                    cleaned_block = clean_non_latin_chars(block_text)

                    # Skip if cleaning removed all meaningful content
                    if cleaned_block and len(cleaned_block.strip()) > 3:
                        text_blocks.append(cleaned_block)

    return text_blocks


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Process a single PDF file and return extracted text using PyMuPDF."""
    try:
        # Open PDF with PyMuPDF
        doc = fitz.open(str(pdf_path))

        # Extract text blocks
        text_blocks = extract_text_blocks(doc)

        # Close the document
        doc.close()

        # Combine and clean blocks
        full_text = []
        for block in text_blocks:
            cleaned_text = clean_text(block)
            # Skip if too short after cleaning
            if cleaned_text and len(cleaned_text) > 10:
                full_text.append(cleaned_text)

        return "\n\n".join(full_text)

    except Exception as e:
        print(f"Error processing {pdf_path.name}: {str(e)}", file=sys.stderr)
        return ""


def main():
    """Main function to process a single PDF file."""
    parser = argparse.ArgumentParser(description="Extract text from a PDF file.")
    parser.add_argument("pdf_path", type=Path, help="Path to the PDF file")
    args = parser.parse_args()

    if not args.pdf_path.exists():
        print(f"Error: File {args.pdf_path} does not exist!", file=sys.stderr)
        sys.exit(1)

    text = extract_text_from_pdf(args.pdf_path)
    print(text)


if __name__ == "__main__":
    main()
