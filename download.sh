#!/bin/bash

# Usage: ./download_pdf.sh <url> [output_filename]

if [ -z "$1" ]; then
    echo "Usage: $0 <url> [output_filename]"
    exit 1
fi

url="$1"
max=$((25 * 1024 * 1024))   # 25 MB in bytes
user_fname="$2"

# Fetch headers once and reuse
headers=$(curl -sI "$url")

# Extract Content-Type (case-insensitive)
ctype=$(echo "$headers" | grep -i "^Content-Type:")
if ! echo "$ctype" | grep -qi "application/pdf"; then
    echo "Error: URL does not point to a PDF (Content-Type is: $ctype)"
    exit 1
fi

# Extract Content-Length (case-insensitive)
clen=$(echo "$headers" | grep -i "^Content-Length:" | awk '{print $2}' | tr -d '\r')

if [ -z "$clen" ]; then
    echo "Error: Server did not provide Content-Length (cannot validate size)."
    exit 1
fi

# Validate size
if [ "$clen" -le "$max" ]; then
    # Determine filename
    if [ -n "$user_fname" ]; then
        fname="$user_fname"
    else
        # Derive filename from URL
        fname=$(basename "$url")
        if [ -z "$fname" ] || [ "$fname" = "/" ]; then
            fname="download.pdf"
        fi
    fi

    #echo "Downloading $fname (size: $clen bytes)..."
    curl -s -L "$url" -o "$fname"

    if [ $? -eq 0 ]; then
        #echo "Download successful. Running extract_pdf_text.py..."
        uv run python ./extract_pdf_text.py "$fname"
    else
        echo "Error: Download failed."
        exit 1
    fi
else
    echo "Error: File size $clen bytes exceeds the 25 MB limit."
    exit 1
fi