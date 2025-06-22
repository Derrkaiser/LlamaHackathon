"""
Test PDF parsing and Llama summarization
"""

import asyncio
import os
import sys
import argparse
from src.analysis.document_parser import DocumentParser, ParsedDocument
from src.core.llama_client import LlamaClient, LlamaConfig, DocumentContext
from config import LLAMA_BASE_URL, LLAMA_MODEL

async def test_pdf_parsing_and_summary(pdf_path: str):
    """Test PDF parsing and Llama summarization"""
    
    print(f"🔍 Testing PDF parsing: {pdf_path}")
    print("=" * 60)
    
    # Step 1: Parse the PDF
    try:
        doc_parser = DocumentParser()
        print("📄 Parsing PDF document...")
        
        parsed_doc = doc_parser.parse_document(pdf_path)
        
        print("✅ PDF parsing successful!")
        print(f"   📁 Filename: {parsed_doc.filename}")
        print(f"   📄 Total Pages: {parsed_doc.total_pages}")
        print(f"   🎫 Requirements Found: {len(parsed_doc.requirements)}")
        print(f"   📊 Summary: {parsed_doc.summary}")
        
        # Display parsed requirements
        print("\n📋 Parsed Requirements:")
        for i, req in enumerate(parsed_doc.requirements, 1):
            print(f"   {i}. {req.title}")
            print(f"      Priority: {req.priority}")
            print(f"      Features: {', '.join(req.features)}")
            print(f"      Description: {req.description[:100]}...")
            print()
        
    except Exception as e:
        print(f"❌ PDF parsing failed: {e}")
        return
    
    # Step 2: Convert to DocumentContext for Llama
    document_context = DocumentContext(
        filename=parsed_doc.filename,
        requirements=[{
            "title": req.title,
            "description": req.description,
            "priority": req.priority,
            "features": req.features,
            "acceptance_criteria": req.acceptance_criteria,
            "technical_notes": req.technical_notes,
            "page_number": req.page_number
        } for req in parsed_doc.requirements],
        summary=parsed_doc.summary,
        total_requirements=len(parsed_doc.requirements)
    )
    
    # Step 3: Test Llama summarization
    try:
        print("🤖 Testing Llama Maverick summarization...")
        
        # Initialize Llama client
        api_key = os.getenv("LLAMA_API_KEY")
        if not api_key:
            print("❌ LLAMA_API_KEY environment variable not set")
            return
        
        config = LlamaConfig(api_key=api_key)
        llama_client = LlamaClient(config)
        
        # Create summary prompt
        summary_prompt = f"""
        Please provide a comprehensive summary of this requirements document:
        
        Document: {document_context.filename}
        Total Requirements: {document_context.total_requirements}
        
        Requirements Details:
        {document_context.summary}
        
        Individual Requirements:
        """
        
        for i, req in enumerate(document_context.requirements, 1):
            summary_prompt += f"""
        Requirement {i}:
        - Title: {req['title']}
        - Priority: {req['priority']}
        - Description: {req['description']}
        - Features: {', '.join(req['features'])}
        - Acceptance Criteria: {', '.join(req['acceptance_criteria'])}
        """
        
        summary_prompt += """
        
        Please provide:
        1. A high-level summary of the document's purpose
        2. Key themes and patterns across the requirements
        3. Priority distribution and focus areas
        4. Technical complexity assessment
        5. Recommendations for presentation focus
        """
        
        print("📝 Sending to Llama Maverick...")
        response = await llama_client._call_llama(summary_prompt)
        
        print("\n✅ Llama Summary Generated!")
        print("=" * 60)
        print(response)
        print("=" * 60)
        
        # Test with a more specific prompt
        print("\n🤖 Testing specific analysis prompt...")
        
        specific_prompt = f"""
        Based on this requirements document, analyze:
        
        Document: {document_context.filename}
        Requirements: {len(document_context.requirements)} total
        
        {document_context.summary}
        
        Please answer these specific questions:
        1. What is the main purpose of this software project?
        2. Which requirements would be most impressive to demonstrate in a live demo?
        3. What technical challenges are implied by these requirements?
        4. How would you structure a 5-minute presentation of these features?
        5. What audience would find this most compelling?
        
        Provide concise, actionable insights.
        """
        
        specific_response = await llama_client._call_llama(specific_prompt)
        
        print("\n✅ Specific Analysis Generated!")
        print("=" * 60)
        print(specific_response)
        print("=" * 60)
        
        await llama_client.close()
        
    except Exception as e:
        print(f"❌ Llama summarization failed: {e}")

async def test_with_sample_pdf():
    """Test with a sample PDF if available"""
    
    # Check for common PDF locations
    possible_paths = [
        "requirements.pdf",
        "sample_requirements.pdf", 
        "test_document.pdf",
        "uploads/requirements.pdf",
        "./requirements.pdf"
    ]
    
    pdf_found = False
    for path in possible_paths:
        if os.path.exists(path):
            print(f"📁 Found PDF: {path}")
            await test_pdf_parsing_and_summary(path)
            pdf_found = True
            break
    
    if not pdf_found:
        print("❌ No PDF found for testing")
        print("Please place a PDF file named 'requirements.pdf' in the project root")
        print("Or update the path in the test script")

def create_sample_pdf():
    """Create a sample PDF for testing (if needed)"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        filename = "sample_requirements.pdf"
        c = canvas.Canvas(filename, pagesize=letter)
        
        # Page 1: User Authentication
        c.drawString(100, 750, "REQUIREMENT 1: User Authentication System")
        c.drawString(100, 720, "Priority: High")
        c.drawString(100, 690, "Description: Implement secure user login and registration system")
        c.drawString(100, 660, "Features:")
        c.drawString(120, 630, "• User registration with email verification")
        c.drawString(120, 600, "• Secure login with password hashing")
        c.drawString(120, 570, "• Password reset functionality")
        c.drawString(100, 540, "Acceptance Criteria:")
        c.drawString(120, 510, "• Users can register with valid email")
        c.drawString(120, 480, "• Passwords are encrypted using bcrypt")
        c.drawString(120, 450, "• Login sessions are secure")
        c.drawString(100, 420, "Technical Notes: Use JWT tokens for session management")
        c.showPage()
        
        # Page 2: Real-time Chat
        c.drawString(100, 750, "REQUIREMENT 2: Real-time Chat Feature")
        c.drawString(100, 720, "Priority: High")
        c.drawString(100, 690, "Description: Enable instant messaging between users")
        c.drawString(100, 660, "Features:")
        c.drawString(120, 630, "• Real-time message sending and receiving")
        c.drawString(120, 600, "• Message history and persistence")
        c.drawString(120, 570, "• Online/offline status indicators")
        c.drawString(100, 540, "Acceptance Criteria:")
        c.drawString(120, 510, "• Messages appear instantly for all users")
        c.drawString(120, 480, "• Chat history is preserved in database")
        c.drawString(120, 450, "• Users can see who is online")
        c.drawString(100, 420, "Technical Notes: Use WebSocket connections for real-time updates")
        c.showPage()
        
        # Page 3: File Upload System
        c.drawString(100, 750, "REQUIREMENT 3: File Upload and Sharing")
        c.drawString(100, 720, "Priority: Medium")
        c.drawString(100, 690, "Description: Allow users to upload and share files")
        c.drawString(100, 660, "Features:")
        c.drawString(120, 630, "• Drag-and-drop file upload")
        c.drawString(120, 600, "• File type validation and security")
        c.drawString(120, 570, "• File sharing with other users")
        c.drawString(100, 540, "Acceptance Criteria:")
        c.drawString(120, 510, "• Files upload successfully")
        c.drawString(120, 480, "• Only allowed file types are accepted")
        c.drawString(120, 450, "• Users can share files with specific users")
        c.drawString(100, 420, "Technical Notes: Store files in cloud storage (AWS S3)")
        c.showPage()
        
        c.save()
        print(f"✅ Created sample PDF: {filename}")
        return filename
        
    except ImportError:
        print("❌ reportlab not installed. Install with: pip install reportlab")
        return None
    except Exception as e:
        print(f"❌ Failed to create sample PDF: {e}")
        return None

def main():
    """Main function with command line argument support"""
    parser = argparse.ArgumentParser(description='Test PDF parsing and Llama summarization')
    parser.add_argument('--pdf', '-p', type=str, help='Path to PDF file to test')
    parser.add_argument('--create-sample', '-s', action='store_true', help='Create a sample PDF for testing')
    
    args = parser.parse_args()
    
    print("🚀 PDF Parsing and Llama Summarization Test")
    print("=" * 60)
    
    # If PDF path is provided, test that specific file
    if args.pdf:
        if os.path.exists(args.pdf):
            print(f"📁 Testing provided PDF: {args.pdf}")
            asyncio.run(test_pdf_parsing_and_summary(args.pdf))
        else:
            print(f"❌ PDF file not found: {args.pdf}")
            return
    
    # If create-sample flag is used, create and test sample PDF
    elif args.create_sample:
        print("📄 Creating sample PDF for testing...")
        sample_pdf = create_sample_pdf()
        if sample_pdf:
            print("\n" + "=" * 60)
            asyncio.run(test_pdf_parsing_and_summary(sample_pdf))
    
    # Otherwise, try to find existing PDFs
    else:
        asyncio.run(test_with_sample_pdf())
        
        # If no PDF found, offer to create a sample
        if not os.path.exists("sample_requirements.pdf"):
            print("\n" + "=" * 60)
            print("📄 No PDF found. Creating sample PDF for testing...")
            sample_pdf = create_sample_pdf()
            if sample_pdf:
                print("\n" + "=" * 60)
                asyncio.run(test_pdf_parsing_and_summary(sample_pdf))
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    main() 