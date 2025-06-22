"""
Sample PDF Format Generator - Shows the expected format for requirement documents
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from reportlab.lib import colors

def create_formatted_sample_pdf():
    """Create a properly formatted sample PDF showing expected structure"""
    
    filename = "sample_requirements_formatted.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.darkblue
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8,
        textColor=colors.darkred
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6
    )
    
    # Page 1: User Authentication System
    story.append(Paragraph("REQUIREMENT 1: User Authentication System", title_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Priority: High", subtitle_style))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("Description:", subtitle_style))
    story.append(Paragraph("Implement a comprehensive user authentication and authorization system that provides secure access to the platform. The system should support multiple authentication methods and maintain user sessions securely.", body_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Features:", subtitle_style))
    story.append(Paragraph("• User registration with email verification", body_style))
    story.append(Paragraph("• Secure login with password hashing (bcrypt)", body_style))
    story.append(Paragraph("• Password reset functionality via email", body_style))
    story.append(Paragraph("• Multi-factor authentication (MFA) support", body_style))
    story.append(Paragraph("• Session management with JWT tokens", body_style))
    story.append(Paragraph("• Role-based access control (RBAC)", body_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Acceptance Criteria:", subtitle_style))
    story.append(Paragraph("• Users can register with valid email addresses", body_style))
    story.append(Paragraph("• Email verification is required before account activation", body_style))
    story.append(Paragraph("• Passwords are encrypted using bcrypt with salt", body_style))
    story.append(Paragraph("• Login sessions are secure and expire appropriately", body_style))
    story.append(Paragraph("• Password reset emails are sent securely", body_style))
    story.append(Paragraph("• MFA can be enabled/disabled by users", body_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Technical Notes:", subtitle_style))
    story.append(Paragraph("Use JWT tokens for session management. Implement rate limiting for login attempts. Store user data in encrypted format. Use OAuth 2.0 for third-party authentication providers.", body_style))
    
    story.append(PageBreak())
    
    # Page 2: Real-time Chat Feature
    story.append(Paragraph("REQUIREMENT 2: Real-time Chat Feature", title_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Priority: High", subtitle_style))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("Description:", subtitle_style))
    story.append(Paragraph("Develop a real-time messaging system that enables instant communication between users. The system should support both one-on-one and group conversations with rich media sharing capabilities.", body_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Features:", subtitle_style))
    story.append(Paragraph("• Real-time message sending and receiving", body_style))
    story.append(Paragraph("• Message history and persistence", body_style))
    story.append(Paragraph("• Online/offline status indicators", body_style))
    story.append(Paragraph("• Typing indicators", body_style))
    story.append(Paragraph("• Message read receipts", body_style))
    story.append(Paragraph("• File and image sharing", body_style))
    story.append(Paragraph("• Group chat functionality", body_style))
    story.append(Paragraph("• Message search and filtering", body_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Acceptance Criteria:", subtitle_style))
    story.append(Paragraph("• Messages appear instantly for all participants", body_style))
    story.append(Paragraph("• Chat history is preserved in database", body_style))
    story.append(Paragraph("• Users can see who is online/offline", body_style))
    story.append(Paragraph("• Typing indicators show when someone is typing", body_style))
    story.append(Paragraph("• Read receipts confirm message delivery", body_style))
    story.append(Paragraph("• Files up to 10MB can be shared", body_style))
    story.append(Paragraph("• Group chats support up to 50 participants", body_style))
    story.append(Paragraph("• Messages can be searched by content", body_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Technical Notes:", subtitle_style))
    story.append(Paragraph("Use WebSocket connections for real-time updates. Implement message queuing for offline users. Use Redis for caching online status. Store messages in MongoDB with indexing for search.", body_style))
    
    story.append(PageBreak())
    
    # Page 3: File Upload and Sharing
    story.append(Paragraph("REQUIREMENT 3: File Upload and Sharing", title_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Priority: Medium", subtitle_style))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("Description:", subtitle_style))
    story.append(Paragraph("Create a secure file management system that allows users to upload, store, and share files with other users. The system should support various file types and provide access control.", body_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Features:", subtitle_style))
    story.append(Paragraph("• Drag-and-drop file upload interface", body_style))
    story.append(Paragraph("• File type validation and security scanning", body_style))
    story.append(Paragraph("• File sharing with specific users or groups", body_style))
    story.append(Paragraph("• File version control and history", body_style))
    story.append(Paragraph("• File preview for common formats", body_style))
    story.append(Paragraph("• Storage quota management", body_style))
    story.append(Paragraph("• File encryption at rest", body_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Acceptance Criteria:", subtitle_style))
    story.append(Paragraph("• Files upload successfully with progress indicator", body_style))
    story.append(Paragraph("• Only allowed file types are accepted", body_style))
    story.append(Paragraph("• Files are scanned for malware", body_style))
    story.append(Paragraph("• Users can share files with specific users", body_style))
    story.append(Paragraph("• File versions are tracked and accessible", body_style))
    story.append(Paragraph("• Common file types can be previewed", body_style))
    story.append(Paragraph("• Storage limits are enforced", body_style))
    story.append(Paragraph("• Files are encrypted in storage", body_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Technical Notes:", subtitle_style))
    story.append(Paragraph("Store files in cloud storage (AWS S3). Use virus scanning service for security. Implement file deduplication. Use CDN for file delivery. Encrypt files with AES-256.", body_style))
    
    story.append(PageBreak())
    
    # Page 4: Dashboard Analytics
    story.append(Paragraph("REQUIREMENT 4: Dashboard Analytics", title_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Priority: Medium", subtitle_style))
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("Description:", subtitle_style))
    story.append(Paragraph("Build a comprehensive analytics dashboard that provides users with insights into their usage patterns, performance metrics, and system statistics. The dashboard should be customizable and real-time.", body_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Features:", subtitle_style))
    story.append(Paragraph("• Real-time data visualization", body_style))
    story.append(Paragraph("• Customizable dashboard widgets", body_style))
    story.append(Paragraph("• Export functionality (PDF, CSV)", body_style))
    story.append(Paragraph("• Scheduled report generation", body_style))
    story.append(Paragraph("• Interactive charts and graphs", body_style))
    story.append(Paragraph("• Performance metrics tracking", body_style))
    story.append(Paragraph("• User activity monitoring", body_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Acceptance Criteria:", subtitle_style))
    story.append(Paragraph("• Dashboard loads within 3 seconds", body_style))
    story.append(Paragraph("• Users can customize widget layout", body_style))
    story.append(Paragraph("• Reports can be exported in multiple formats", body_style))
    story.append(Paragraph("• Scheduled reports are delivered on time", body_style))
    story.append(Paragraph("• Charts are interactive and responsive", body_style))
    story.append(Paragraph("• Performance metrics are accurate", body_style))
    story.append(Paragraph("• User activity is tracked in real-time", body_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Technical Notes:", subtitle_style))
    story.append(Paragraph("Use Chart.js for visualizations. Implement data caching with Redis. Use WebSockets for real-time updates. Store analytics data in time-series database (InfluxDB).", body_style))
    
    # Build the PDF
    doc.build(story)
    print(f"✅ Created formatted sample PDF: {filename}")
    return filename

def print_expected_format():
    """Print the expected format guidelines"""
    
    print("📋 EXPECTED PDF FORMAT FOR REQUIREMENT DOCUMENTS")
    print("=" * 60)
    print()
    print("🎯 STRUCTURE: Each page should represent ONE requirement ticket")
    print("📄 FORMAT: Clear sections with consistent formatting")
    print()
    print("📝 REQUIRED SECTIONS (in order):")
    print("   1. TITLE: 'REQUIREMENT X: [Feature Name]'")
    print("   2. PRIORITY: 'Priority: [High/Medium/Low]'")
    print("   3. DESCRIPTION: Brief overview of the requirement")
    print("   4. FEATURES: Bullet points of specific features")
    print("   5. ACCEPTANCE CRITERIA: Bullet points of success criteria")
    print("   6. TECHNICAL NOTES: Implementation details (optional)")
    print()
    print("✅ OPTIMAL FORMATTING:")
    print("   • Use clear headings and subheadings")
    print("   • Use bullet points (•) for lists")
    print("   • Keep descriptions concise but detailed")
    print("   • Use consistent terminology")
    print("   • Include specific technical details")
    print()
    print("❌ AVOID:")
    print("   • Dense paragraphs without structure")
    print("   • Inconsistent formatting across pages")
    print("   • Vague or ambiguous requirements")
    print("   • Missing priority levels")
    print("   • No clear acceptance criteria")
    print()
    print("📊 PARSING EXPECTATIONS:")
    print("   • Title extraction from first line")
    print("   • Priority detection from 'Priority:' keyword")
    print("   • Feature extraction from bullet points")
    print("   • Acceptance criteria from 'Acceptance Criteria:' section")
    print("   • Technical notes from 'Technical Notes:' section")
    print()

if __name__ == "__main__":
    print_expected_format()
    
    print("🚀 Creating formatted sample PDF...")
    sample_pdf = create_formatted_sample_pdf()
    
    if sample_pdf:
        print(f"\n✅ Sample PDF created: {sample_pdf}")
        print("📄 This PDF shows the optimal format for requirement documents")
        print("🧪 You can test it with: python test_pdf_parsing.py --pdf sample_requirements_formatted.pdf")
    else:
        print("❌ Failed to create sample PDF") 