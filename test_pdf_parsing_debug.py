#!/usr/bin/env python3
"""
Debug script to test PDF parsing and see raw text extraction
"""

import os
import sys
sys.path.append('src')

from analysis.document_parser import DocumentParser
import pdfplumber

def test_raw_pdf_extraction():
    """Test raw PDF text extraction to see what we're working with"""
    
    pdf_path = "Calculator_Requirements_Doc.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"PDF file not found: {pdf_path}")
        return
    
    print("=== RAW PDF TEXT EXTRACTION ===")
    
    # Test with pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            print(f"\n--- PAGE {page_num} ---")
            text = page.extract_text()
            if text:
                print("RAW TEXT:")
                print(text)
                print("\n" + "="*50)
            else:
                print("No text extracted from this page")

def test_structured_parsing():
    """Test the structured parsing to see what's happening"""
    
    pdf_path = "Calculator_Requirements_Doc.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"PDF file not found: {pdf_path}")
        return
    
    print("\n=== STRUCTURED PARSING TEST ===")
    
    parser = DocumentParser()
    
    try:
        parsed_doc = parser.parse_document(pdf_path)
        
        print(f"Document: {parsed_doc.filename}")
        print(f"Total pages: {parsed_doc.total_pages}")
        print(f"Requirements found: {len(parsed_doc.requirements)}")
        print(f"Summary: {parsed_doc.summary}")
        
        for i, req in enumerate(parsed_doc.requirements, 1):
            print(f"\n--- REQUIREMENT {i} ---")
            print(f"Page: {req.page_number}")
            print(f"Title: {req.title}")
            print(f"Priority: {req.priority}")
            print(f"Description: {req.description}")
            print(f"Features ({len(req.features)}): {req.features}")
            print(f"Acceptance Criteria ({len(req.acceptance_criteria)}): {req.acceptance_criteria}")
            print(f"Technical Notes: {req.technical_notes}")
            print(f"Raw text length: {len(req.raw_text)}")
            
    except Exception as e:
        print(f"Error parsing document: {e}")
        import traceback
        traceback.print_exc()

def test_text_cleaning():
    """Test the text cleaning function specifically"""
    
    sample_text = """REQUIREMENT 1: Calculator Display Component
Priority: High
Description:
 Provide a single, always-visible display panel that shows the current input and/or result. The panel must resize gracefully across devices while maintaining readability.
Features:
 • Numeric output up to 12 digits (defaults to scientific notation beyond)
 • Distinct style for "in-progress" expression vs. final result
 • Auto-scroll or shrink font when length exceeds display width
 • Read-only interaction (no manual typing into display)
Acceptance Criteria:
 • Input "12 + 7 =" renders 19 in large font
 • Long operations (e.g., 123456789 * 99999) wrap or shrink without overflowing container
 • Display resets to "0" after "AC" is pressed
Technical Notes:
 Use a dedicated <Display /> React component that accepts a value prop. Implement dynamic font sizing with CSS clamp() or calc() and test at 320 px width."""
    
    print("=== TEXT CLEANING TEST ===")
    print("ORIGINAL TEXT:")
    print(sample_text)
    print("\n" + "="*50)
    
    # Test the current cleaning method
    lines = sample_text.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line:
            cleaned_lines.append(line)
    
    print("CLEANED TEXT (line by line):")
    for line in cleaned_lines:
        print(f"'{line}'")
    
    print("\n" + "="*50)
    
    # Test the problematic cleaning method
    problematic_cleaned = " ".join(sample_text.split())
    print("PROBLEMATIC CLEANED TEXT:")
    print(problematic_cleaned)

if __name__ == "__main__":
    test_raw_pdf_extraction()
    test_structured_parsing()
    test_text_cleaning() 