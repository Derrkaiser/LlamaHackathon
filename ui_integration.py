"""
UI Integration - Connects Streamlit UI to unified processing pipeline
"""

import asyncio
import os
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional
import streamlit as st

from src.core.unified_processor import UnifiedProcessor

async def process_demo_request(ui_inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process demo request using the unified processor
    
    Args:
        ui_inputs: Dictionary containing all UI inputs from Streamlit
        
    Returns:
        Dictionary with presentation script, agent execution plan, and analysis summary
    """
    
    try:
        # Extract inputs
        github_url = ui_inputs.get("github_url", "")
        uploaded_file = ui_inputs.get("uploaded_file")
        pdf_path = ui_inputs.get("pdf_path", "")
        llama_api_key = ui_inputs.get("llama_api_key")
        
        # Validate required inputs
        if not llama_api_key:
            raise ValueError("Llama API key is required")
        
        if not github_url and not (uploaded_file or pdf_path):
            raise ValueError("Either GitHub URL or requirements document is required")
        
        # Set environment variable for Llama API key
        os.environ["LLAMA_API_KEY"] = llama_api_key
        
        # Create UI preferences dictionary
        ui_preferences = {
            "demo_duration": ui_inputs.get("demo_duration", 5),
            "audience_type": ui_inputs.get("audience_type", "General"),
            "custom_audience": ui_inputs.get("custom_audience", ""),
            "demo_purpose": ui_inputs.get("demo_purpose", "Feature Showcase"),
            "custom_purpose": ui_inputs.get("custom_purpose", ""),
            "focus_areas": ui_inputs.get("focus_areas", []),
            "custom_focus": ui_inputs.get("custom_focus", ""),
            "include_code_analysis": ui_inputs.get("include_code_analysis", True),
            "include_risk_assessment": ui_inputs.get("include_risk_assessment", True)
        }
        
        # Initialize unified processor (no parameters needed)
        processor = UnifiedProcessor()
        
        # Process the complete request using the new interface
        result = await processor.process_demo_request(
            github_url=github_url,
            requirements_file=uploaded_file,
            requirements_path=pdf_path if pdf_path else None,
            audience=ui_preferences.get("audience_type", "Mixed Technical & Business"),
            purpose=ui_preferences.get("demo_purpose", "Feature Showcase"),
            demo_duration=ui_preferences.get("demo_duration", 5)
        )
        
        # Return results in the expected format
        return {
            "presentation_script": result.get("presentation_script", ""),
            "agent_execution_plan": result.get("demo_plan", {}),
            "analysis_summary": {
                "requirements_count": result.get("requirements_summary", {}).get("count", 0),
                "features_count": len(result.get("github_summary", {}).get("key_features", [])),
                "complexity": "Medium",
                "risk_level": "Low",
                "summary": f"Generated presentation with {len(result.get('avatar_script', {}).get('presentation', {}).get('segments', []))} segments",
                "presentation_duration": result.get("avatar_script", {}).get("timing", {}).get("total_duration", 0)
            },
            "document_context": {
                "filename": "requirements.pdf",
                "requirements_count": result.get("requirements_summary", {}).get("count", 0),
                "summary": "Requirements processed successfully"
            },
            "codebase_context": {
                "architecture": result.get("github_summary", {}).get("architecture", "Unknown"),
                "features": result.get("github_summary", {}).get("key_features", []),
                "components": result.get("github_summary", {}).get("tech_stack", [])
            }
        }
        
    except Exception as e:
        raise Exception(f"Demo request processing failed: {str(e)}")

# Legacy compatibility - keep the old class for backward compatibility
class UIIntegration:
    """Legacy UI integration class - now uses UnifiedProcessor"""
    
    def __init__(self):
        pass
    
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
        """Legacy method - now uses unified processor"""
        
        ui_inputs = {
            "github_url": github_url,
            "uploaded_file": uploaded_file,
            "pdf_path": pdf_path,
            "demo_duration": demo_duration,
            "audience_type": audience_type,
            "custom_audience": custom_audience,
            "demo_purpose": demo_purpose,
            "custom_purpose": custom_purpose,
            "focus_areas": focus_areas,
            "custom_focus": custom_focus,
            "llama_api_key": llama_api_key,
            "demo_url": demo_url,
            "include_code_analysis": include_code_analysis,
            "include_risk_assessment": include_risk_assessment
        }
        
        return await process_demo_request(ui_inputs) 