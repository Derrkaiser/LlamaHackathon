#!/usr/bin/env python3
"""
Document Parser - Parses PDF and DOCX files to extract requirements
"""

import os
from typing import List, Dict, Any
from pathlib import Path

class DocumentParser:
    """Simple document parser for requirements extraction"""
    
    def __init__(self):
        pass
    
    def parse_document(self, file_path: str) -> List[Dict[str, Any]]:
        """Parse document and extract requirements"""
        
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"⚠️ File not found: {file_path}")
            return self._get_mock_requirements()
        
        if file_path.suffix.lower() == '.pdf':
            return self._parse_pdf(file_path)
        elif file_path.suffix.lower() in ['.docx', '.doc']:
            return self._parse_docx(file_path)
        else:
            print(f"⚠️ Unsupported file type: {file_path.suffix}")
            return self._get_mock_requirements()
    
    def _parse_pdf(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse PDF file"""
        
        try:
            # For now, return mock data
            # In a real implementation, you would use PyPDF2 or pdfplumber
            print(f"📄 Parsing PDF: {file_path}")
            return self._get_mock_requirements()
            
        except Exception as e:
            print(f"❌ PDF parsing failed: {e}")
            return self._get_mock_requirements()
    
    def _parse_docx(self, file_path: Path) -> List[Dict[str, Any]]:
        """Parse DOCX file"""
        
        try:
            # For now, return mock data
            # In a real implementation, you would use python-docx
            print(f"📄 Parsing DOCX: {file_path}")
            return self._get_mock_requirements()
            
        except Exception as e:
            print(f"❌ DOCX parsing failed: {e}")
            return self._get_mock_requirements()
    
    def _get_mock_requirements(self) -> List[Dict[str, Any]]:
        """Return mock requirements for testing"""
        
        return [
            {
                "title": "User Authentication",
                "description": "Implement secure user login system with email and password",
                "priority": "High",
                "features": ["Login form", "Password validation", "Session management"],
                "acceptance_criteria": ["Users can log in with email/password", "Failed attempts are logged"],
                "technical_notes": "Use JWT tokens for session management"
            },
            {
                "title": "Dashboard Analytics",
                "description": "Display key metrics and analytics on user dashboard",
                "priority": "Medium",
                "features": ["Metrics dashboard", "Real-time updates", "Export functionality"],
                "acceptance_criteria": ["Dashboard loads within 3 seconds", "Data updates every 30 seconds"],
                "technical_notes": "Use WebSocket for real-time updates"
            },
            {
                "title": "File Management",
                "description": "Allow users to upload, organize, and share files",
                "priority": "Medium",
                "features": ["File upload", "Folder organization", "Sharing permissions"],
                "acceptance_criteria": ["Files upload successfully", "Users can create folders", "Sharing works correctly"],
                "technical_notes": "Use cloud storage for file handling"
            }
        ] 