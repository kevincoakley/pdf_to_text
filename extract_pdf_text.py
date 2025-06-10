#!/usr/bin/env python3
"""
Extract high-quality text from academic PDF papers using unstructured library.
Processes all PDFs in the pdf/ directory and saves results to results/ directory.
"""

import os
import re
from pathlib import Path
from unstructured.partition.pdf import partition_pdf


def is_formula_or_equation(text: str) -> bool:
    """Detect if text contains mathematical formulas or equations."""
    # Skip short text that's unlikely to be standalone formulas
    if len(text.strip()) < 5:
        return False
    
    # Common math indicators
    math_patterns = [
        r'\b[a-zA-Z]\s*[=<>≤≥≠]',  # Variables with operators (a = b, x ≤ y)
        r'\([0-9]+\)',              # Numbered equations like (1), (2)
        r'∑|∏|∫|∂|∇|α|β|γ|δ|ε|θ|λ|μ|π|σ|τ|φ|ψ|ω',  # Math symbols
        r'\b(exp|log|sin|cos|tan|max|min|argmax|argmin)\s*\(',  # Math functions
        r'p\s*\([^)]*\)\s*[=<>]',   # Probability notation p(x) =
        r'\bEq\.?\s*[0-9]',        # Equation references
        r'\bmult\s*\(',            # Multinomial functions
        r'Z[αβγδε]|Z_',            # Normalization constants
        r'[A-Z][A-Za-z]*\s*[⇠∼]',  # Distribution notation A ~ 
        r'\b[A-Z][a-z]*\s*=\s*argmax',  # Optimization notation
    ]
    
    # Check for math patterns
    for pattern in math_patterns:
        if re.search(pattern, text):
            return True
    
    # Check for high density of mathematical characters
    math_chars = len(re.findall(r'[=<>≤≥≠∑∏∫∂∇αβγδεθλμπστφψω⇠∼]', text))
    if len(text) > 0 and math_chars / len(text) > 0.1:  # More than 10% math symbols
        return True
    
    return False


def clean_text(text: str) -> str:
    """Clean and fix common PDF extraction issues in academic papers."""
    # Fix hyphenated words (handles various patterns)
    text = re.sub(r'(\w)-\s+(\w)', r'\1\2', text)  # Fix "word- word" -> "wordword"
    text = re.sub(r'(\w)-\s*\n\s*(\w)', r'\1\2', text)  # Fix hyphenated across lines
    
    # Fix common PDF extraction issues
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)  # Fix merged words like "wordWord"
    text = re.sub(r'\s+', ' ', text)  # Normalize whitespace (after hyphen fixes)
    
    # Preserve academic formatting
    text = re.sub(r'\n\s*•\s*', '\n• ', text)  # Fix bullet points
    text = re.sub(r'\n\s*(\d+\.)\s*', r'\n\1 ', text)  # Fix numbered lists
    
    return text.strip()


def group_elements_into_paragraphs(elements):
    """Group elements into paragraphs based on their types and content."""
    paragraphs = []
    current_paragraph = []
    
    for element in elements:
        element_type = str(type(element).__name__)
        element_text = str(element).strip()
        
        # Skip empty elements
        if not element_text:
            continue
            
        # Skip mathematical formulas and equations
        if is_formula_or_equation(element_text):
            continue
            
        # Titles and headers should be on their own lines
        if element_type in ['Title', 'Header']:
            # Finish current paragraph first
            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
            # Add title/header as its own paragraph
            paragraphs.append(element_text)
        
        # Page breaks - just finish current paragraph, don't add content
        elif element_type == 'PageBreak':
            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
        
        # For regular text, continue building current paragraph or start new one
        elif element_type in ['Text', 'NarrativeText']:
            # If this looks like a new paragraph (starts with capital, ends with period)
            # and we have existing content, start new paragraph
            if (current_paragraph and 
                len(element_text) > 50 and  # Substantial text
                element_text[0].isupper() and  # Starts with capital
                current_paragraph[-1].endswith(('.', '!', '?'))):
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = [element_text]
            else:
                current_paragraph.append(element_text)
        
        # For other elements (lists, tables, etc.), treat as separate paragraphs
        else:
            if current_paragraph:
                paragraphs.append(' '.join(current_paragraph))
                current_paragraph = []
            paragraphs.append(element_text)
    
    # Add any remaining content
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))
    
    return paragraphs


def process_pdf(pdf_path: Path, output_dir: Path) -> None:
    """Process a single PDF file and extract structured text."""
    print(f"Processing: {pdf_path.name}")
    
    try:
        # Use high-quality extraction strategy for academic papers
        elements = partition_pdf(
            filename=str(pdf_path),
            strategy="hi_res",  # High resolution for better quality
            infer_table_structure=True,  # Extract table structure
            extract_images_in_pdf=False,  # Focus on text, not images
            include_page_breaks=True,  # Preserve page structure
        )
        
        # Group elements into paragraphs
        paragraphs = group_elements_into_paragraphs(elements)
        
        # Save plain text output with cleaning - one paragraph per line
        text_output_file = output_dir / f"{pdf_path.stem}.txt"
        with open(text_output_file, 'w', encoding='utf-8') as f:
            f.write(f"# {pdf_path.name}\n\n")
            for paragraph in paragraphs:
                cleaned_text = clean_text(paragraph)
                # Skip if it's a formula or too short
                if (cleaned_text and 
                    len(cleaned_text) > 10 and 
                    not is_formula_or_equation(cleaned_text)):
                    f.write(cleaned_text + "\n\n")
        
        print(f"✓ Completed: {pdf_path.name} -> {text_output_file.name}")
        
    except Exception as e:
        print(f"✗ Error processing {pdf_path.name}: {str(e)}")


def main():
    """Main function to process all PDFs in the pdf directory."""
    # Set up directories
    pdf_dir = Path("pdf")
    output_dir = Path("results")
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # Check if pdf directory exists
    if not pdf_dir.exists():
        print(f"Error: {pdf_dir} directory does not exist!")
        return
    
    # Find all PDF files
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {pdf_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF files to process")
    print(f"Output will be saved to: {output_dir.absolute()}")
    print("-" * 60)
    
    # Process each PDF with error handling
    success_count = 0
    error_count = 0
    
    for pdf_file in sorted(pdf_files):
        try:
            process_pdf(pdf_file, output_dir)
            success_count += 1
        except Exception as e:
            print(f"✗ Failed to process {pdf_file.name}: {str(e)}")
            error_count += 1
            continue
    
    print("-" * 60)
    print(f"Processing complete! Results saved in {output_dir.absolute()}")
    print(f"Successfully processed: {success_count} files")
    print(f"Failed to process: {error_count} files")


if __name__ == "__main__":
    main()