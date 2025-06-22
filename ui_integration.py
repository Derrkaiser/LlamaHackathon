"""
UI Integration - Connects Streamlit UI to existing PDF parsing and Llama functionality
"""

import asyncio
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
import streamlit as st

from src.analysis.document_parser import DocumentParser
from src.core.llama_client import LlamaClient, LlamaConfig, DocumentContext, CodebaseContext, PresentationRequest

class UIIntegration:
    """Handles integration between UI inputs and backend processing"""
    
    def __init__(self):
        self.document_parser = DocumentParser()
    
    async def process_ui_inputs(
        self,
        github_url: str,
        uploaded_file: Optional[Any],
        pdf_path: str,
        demo_duration: int,
        audience_type: str,
        custom_audience: str,
        demo_purpose: str,
        custom_purpose: str,
        focus_areas: list,
        custom_focus: str,
        llama_api_key: str,
        demo_url: str = None,
        include_code_analysis: bool = True,
        include_risk_assessment: bool = True
    ) -> Dict[str, Any]:
        """Process all UI inputs and generate presentation"""
        
        try:
            # Step 1: Initialize Llama client
            config = LlamaConfig(api_key=llama_api_key)
            llama_client = LlamaClient(config)
            
            # Step 2: Process requirements document
            document_context = await self._process_requirements(
                uploaded_file, pdf_path
            )
            
            # Step 3: Process codebase (placeholder for partner's integration)
            codebase_context = await self._process_codebase(github_url)
            
            # Step 4: Build presentation request
            presentation_request = self._build_presentation_request(
                demo_duration, audience_type, custom_audience,
                demo_purpose, custom_purpose, focus_areas, custom_focus
            )
            
            # Step 5: Generate presentation script
            presentation_script = await llama_client.generate_presentation_script(
                codebase_context=codebase_context,
                document_context=document_context,
                user_prompt=self._build_user_prompt(
                    audience_type, custom_audience, demo_purpose, custom_purpose
                ),
                request=presentation_request
            )
            
            # Step 6: Generate agent execution plan
            agent_execution_plan = await llama_client.generate_agent_execution_plan(
                codebase_context=codebase_context,
                document_context=document_context,
                user_prompt=self._build_user_prompt(
                    audience_type, custom_audience, demo_purpose, custom_purpose
                ),
                presentation_script=presentation_script
            )
            
            # Step 7: Generate analysis summary
            analysis_summary = await self._generate_analysis_summary(
                llama_client, document_context, codebase_context
            )
            
            await llama_client.close()
            
            return {
                "presentation_script": presentation_script,
                "agent_execution_plan": agent_execution_plan,
                "analysis_summary": analysis_summary,
                "document_context": document_context,
                "codebase_context": codebase_context
            }
            
        except Exception as e:
            raise Exception(f"Processing failed: {str(e)}")
    
    async def _process_requirements(
        self, uploaded_file: Optional[Any], pdf_path: str
    ) -> DocumentContext:
        """Process requirements document from UI input"""
        
        if uploaded_file:
            # Save uploaded file to temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                temp_pdf_path = tmp_file.name
            
            try:
                parsed_doc = await self.document_parser.parse_pdf(temp_pdf_path)
                return DocumentContext(
                    filename=uploaded_file.name,
                    requirements=parsed_doc.requirements,
                    summary=parsed_doc.summary,
                    total_requirements=len(parsed_doc.requirements)
                )
            finally:
                # Clean up temp file
                os.unlink(temp_pdf_path)
        
        elif pdf_path and os.path.exists(pdf_path):
            parsed_doc = await self.document_parser.parse_pdf(pdf_path)
            return DocumentContext(
                filename=os.path.basename(pdf_path),
                requirements=parsed_doc.requirements,
                summary=parsed_doc.summary,
                total_requirements=len(parsed_doc.requirements)
            )
        
        else:
            # Create mock document context for demo
            return DocumentContext(
                filename="demo_requirements.pdf",
                requirements=[
                    {
                        "title": "User Authentication",
                        "priority": "High",
                        "description": "Implement secure user login system",
                        "features": ["Login", "Registration", "Password Reset"],
                        "acceptance_criteria": ["Users can login", "Passwords are secure"]
                    }
                ],
                summary="Demo requirements for hackathon presentation",
                total_requirements=1
            )
    
    async def _process_codebase(self, github_url: str) -> CodebaseContext:
        """Process codebase from GitHub URL (placeholder for partner's integration)"""
        
        # This would integrate with your partner's GitHub analysis
        # For now, return mock data
        return CodebaseContext(
            architecture="React + Node.js + MongoDB",
            main_features=["User Authentication", "Real-time Chat", "File Upload"],
            dependencies=["react", "express", "mongodb", "socket.io"],
            key_components=["AuthService", "ChatComponent", "FileManager"],
            user_flows=["Login → Dashboard → Chat → File Upload"]
        )
    
    def _build_presentation_request(
        self,
        demo_duration: int,
        audience_type: str,
        custom_audience: str,
        demo_purpose: str,
        custom_purpose: str,
        focus_areas: list,
        custom_focus: str
    ) -> PresentationRequest:
        """Build presentation request from UI inputs"""
        
        # Determine audience
        audience = custom_audience if audience_type == "Custom" else audience_type
        
        # Determine purpose
        purpose = custom_purpose if demo_purpose == "Custom" else demo_purpose
        
        # Process focus areas
        processed_focus_areas = focus_areas.copy()
        if "Custom" in focus_areas and custom_focus:
            processed_focus_areas.remove("Custom")
            processed_focus_areas.append(custom_focus)
        
        return PresentationRequest(
            purpose=purpose,
            audience=audience,
            duration=demo_duration,
            focus_areas=processed_focus_areas,
            demo_requirements=["Live demo", "Code walkthrough", "Feature showcase"]
        )
    
    def _build_user_prompt(
        self,
        audience_type: str,
        custom_audience: str,
        demo_purpose: str,
        custom_purpose: str
    ) -> str:
        """Build user prompt for Llama"""
        
        audience = custom_audience if audience_type == "Custom" else audience_type
        purpose = custom_purpose if demo_purpose == "Custom" else demo_purpose
        
        return f"""
        Create a compelling presentation for:
        - Audience: {audience}
        - Purpose: {purpose}
        
        The presentation should be engaging, technically accurate, and demonstrate the value of the application effectively.
        """
    
    async def _generate_analysis_summary(
        self,
        llama_client: LlamaClient,
        document_context: DocumentContext,
        codebase_context: CodebaseContext
    ) -> Dict[str, Any]:
        """Generate analysis summary using Llama"""
        
        summary_prompt = f"""
        Analyze this project and provide a summary:
        
        Requirements: {document_context.summary}
        Codebase: {codebase_context.architecture}
        Features: {', '.join(codebase_context.main_features)}
        
        Provide:
        1. Key insights about the project
        2. Technical complexity assessment
        3. Demo recommendations
        4. Risk factors to consider
        """
        
        try:
            response = await llama_client._call_llama(summary_prompt)
            return {
                "summary": response,
                "requirements_count": document_context.total_requirements,
                "features_count": len(codebase_context.main_features),
                "complexity": "Medium",  # This could be determined by Llama
                "risk_level": "Low"      # This could be determined by Llama
            }
        except Exception as e:
            return {
                "summary": f"Analysis summary could not be generated: {str(e)}",
                "requirements_count": document_context.total_requirements,
                "features_count": len(codebase_context.main_features),
                "complexity": "Medium",
                "risk_level": "Low"
            }

# Convenience function for Streamlit
async def process_demo_request(ui_inputs: Dict[str, Any]) -> Dict[str, Any]:
    """Process demo request from Streamlit UI"""
    integration = UIIntegration()
    return await integration.process_ui_inputs(**ui_inputs) 