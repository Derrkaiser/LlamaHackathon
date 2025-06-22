"""
Llama 4 Maverick Client - Handles API interactions for presentation generation
"""

import json
import os
from typing import Dict, List, Any
from dataclasses import dataclass
from pydantic import BaseModel
from llama_api_client import AsyncLlamaAPIClient
from dotenv import load_dotenv

load_dotenv()

@dataclass
class LlamaConfig:
    """Configuration for Llama 4 Maverick client"""
    api_key: str
    base_url: str = "https://api.llama-api.com"
    model: str = "Llama-4-Maverick-17B-128E-Instruct-FP8"
    max_tokens: int = 4096
    temperature: float = 0.7

class CodebaseContext(BaseModel):
    """Structured context from codebase analysis"""
    architecture: str
    main_features: List[str]
    dependencies: List[str]
    key_components: List[str]
    user_flows: List[str]

class DocumentContext(BaseModel):
    """Structured context from requirement documents"""
    filename: str
    requirements: List[Dict[str, Any]]
    summary: str
    total_requirements: int

class PresentationRequest(BaseModel):
    """Request for presentation generation"""
    purpose: str
    audience: str
    duration: int  # minutes
    focus_areas: List[str]
    demo_requirements: List[str]

class LlamaClient:
    """Main client for Llama 4 Maverick interactions"""
    
    def __init__(self, config: LlamaConfig):
        self.config = config
        self.client = AsyncLlamaAPIClient(api_key=config.api_key)
    
    async def generate_presentation_script(
        self, 
        codebase_context: CodebaseContext,
        document_context: DocumentContext,
        user_prompt: str,
        request: PresentationRequest
    ) -> Dict[str, Any]:
        """Generate presentation script based on combined context"""
        
        # Build comprehensive context for Llama
        context_prompt = self._build_presentation_context(
            codebase_context, document_context, user_prompt, request
        )
        
        response = await self._call_llama(context_prompt, system_prompt="""
        You are an expert presentation designer and technical communicator. Create compelling presentation scripts that:
        1. Match the audience's technical level and interests
        2. Highlight the most relevant features from the codebase
        3. Tell a compelling story that connects requirements to implementation
        4. Include specific demo scenarios with clear instructions
        5. Provide timing and flow recommendations
        
        Structure the presentation with clear sections, timing, and actionable demo instructions.
        """)
        
        return self._parse_presentation_script(response)
    
    async def generate_agent_execution_plan(
        self, 
        codebase_context: CodebaseContext,
        document_context: DocumentContext,
        user_prompt: str,
        presentation_script: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate agent execution plan for demo orchestration"""
        
        context_prompt = self._build_agent_planning_context(
            codebase_context, document_context, user_prompt, presentation_script
        )
        
        response = await self._call_llama(context_prompt, system_prompt="""
        You are an expert in software demos and agent orchestration. Create detailed agent execution plans that:
        1. Define which agents are needed for each demo scenario
        2. Specify the sequence and timing of agent actions
        3. Include browser automation instructions
        4. Define success criteria and error handling
        5. Coordinate with avatar presentation timing
        6. Plan visual generation and display
        
        Provide structured, executable plans that can be used by automation systems.
        """)
        
        return self._parse_agent_execution_plan(response)
    
    async def _call_llama(self, prompt: str, system_prompt: str = "") -> str:
        """Make API call to Llama 4 Maverick using the working client"""
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=messages
            )
            
            # Extract the text content from the response
            if hasattr(response, 'choices') and len(response.choices) > 0:
                choice = response.choices[0]
                if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                    return choice.message.content
            
            # If response structure is different, try to extract content
            if hasattr(response, 'completion_message'):
                completion = response.completion_message
                if hasattr(completion, 'content'):
                    content = completion.content
                    if hasattr(content, 'text'):
                        return content.text
                    elif isinstance(content, str):
                        return content
            
            # Fallback: return the full response if we can't extract content
            return str(response)
            
        except Exception as e:
            raise Exception(f"Llama API call failed: {str(e)}")
    
    def _build_presentation_context(
        self, 
        codebase_context: CodebaseContext,
        document_context: DocumentContext,
        user_prompt: str,
        request: PresentationRequest
    ) -> str:
        """Build comprehensive context for presentation generation"""
        
        return f"""
        Generate a presentation script based on the following context:
        
        === USER PROMPT ===
        {user_prompt}
        
        === PRESENTATION REQUEST ===
        Purpose: {request.purpose}
        Audience: {request.audience}
        Duration: {request.duration} minutes
        Focus Areas: {', '.join(request.focus_areas)}
        Demo Requirements: {', '.join(request.demo_requirements)}
        
        === CODEBASE ANALYSIS ===
        Architecture: {codebase_context.architecture}
        Main Features: {', '.join(codebase_context.main_features)}
        Dependencies: {', '.join(codebase_context.dependencies)}
        Key Components: {', '.join(codebase_context.key_components)}
        User Flows: {', '.join(codebase_context.user_flows)}
        
        === REQUIREMENTS DOCUMENT ===
        Document: {document_context.filename}
        Summary: {document_context.summary}
        Total Requirements: {document_context.total_requirements}
        
        Requirements Details:
        {json.dumps(document_context.requirements, indent=2)}
        
        Create a compelling presentation that:
        1. Addresses the user's specific prompt and requirements
        2. Shows how the codebase implements the documented requirements
        3. Demonstrates key features with clear demo scenarios
        4. Is tailored to the specified audience and duration
        5. Includes timing, flow, and visual recommendations
        """
    
    def _build_agent_planning_context(
        self,
        codebase_context: CodebaseContext,
        document_context: DocumentContext,
        user_prompt: str,
        presentation_script: Dict[str, Any]
    ) -> str:
        """Build context for agent execution planning"""
        
        return f"""
        Create an agent execution plan for the following presentation:
        
        === USER PROMPT ===
        {user_prompt}
        
        === CODEBASE CONTEXT ===
        Architecture: {codebase_context.architecture}
        Main Features: {', '.join(codebase_context.main_features)}
        Key Components: {', '.join(codebase_context.key_components)}
        
        === PRESENTATION SCRIPT ===
        {json.dumps(presentation_script, indent=2)}
        
        === REQUIREMENTS CONTEXT ===
        Document: {document_context.filename}
        Requirements: {json.dumps(document_context.requirements, indent=2)}
        
        Create a detailed agent execution plan that:
        1. Defines which agents (browser automation, visual generation, etc.) are needed
        2. Specifies the exact sequence and timing of actions
        3. Includes precise browser automation instructions
        4. Defines success criteria and error handling
        5. Coordinates with avatar presentation timing
        6. Plans visual generation and display timing
        
        Focus on creating executable, step-by-step instructions for each demo scenario.
        """
    
    def _parse_presentation_script(self, response: str) -> Dict[str, Any]:
        """Parse Llama response into structured presentation script"""
        
        # For now, return a structured format
        # In production, you'd parse the response more intelligently
        return {
            "title": "Generated Presentation",
            "sections": [
                {
                    "title": "Introduction",
                    "duration": 60,
                    "content": "Introduction content",
                    "demo_trigger": None,
                    "visual_cue": None
                },
                {
                    "title": "Key Features Demo",
                    "duration": 180,
                    "content": "Feature demonstration content",
                    "demo_trigger": "start_feature_demo",
                    "visual_cue": "show_architecture_diagram"
                }
            ],
            "total_duration": 240,
            "key_points": ["Point 1", "Point 2", "Point 3"],
            "demo_scenarios": ["Scenario 1", "Scenario 2"],
            "visual_elements": ["Diagram 1", "Chart 1"]
        }
    
    def _parse_agent_execution_plan(self, response: str) -> Dict[str, Any]:
        """Parse Llama response into structured agent execution plan"""
        
        # For now, return a structured format
        # In production, you'd parse the response more intelligently
        return {
            "agents_required": ["browser_automator", "visual_generator", "tavus_coordinator"],
            "execution_sequence": [
                {
                    "step": 1,
                    "agent": "tavus_coordinator",
                    "action": "start_presentation",
                    "duration": 30,
                    "dependencies": []
                },
                {
                    "step": 2,
                    "agent": "browser_automator",
                    "action": "navigate_to_app",
                    "duration": 10,
                    "dependencies": ["tavus_coordinator"]
                },
                {
                    "step": 3,
                    "agent": "visual_generator",
                    "action": "show_architecture_diagram",
                    "duration": 15,
                    "dependencies": ["browser_automator"]
                }
            ],
            "demo_scenarios": [
                {
                    "name": "Feature Demo 1",
                    "browser_actions": ["click_button", "fill_form", "verify_result"],
                    "visual_triggers": ["show_diagram", "highlight_feature"],
                    "success_criteria": ["page_loaded", "feature_visible"],
                    "error_handling": ["retry_action", "show_fallback"]
                }
            ],
            "timing_coordination": {
                "avatar_pauses": [60, 180, 300],
                "demo_triggers": [90, 210, 330],
                "visual_cues": [75, 195, 315]
            }
        }
    
    async def close(self):
        """Close the client"""
        # The AsyncLlamaAPIClient doesn't need explicit closing
        pass 