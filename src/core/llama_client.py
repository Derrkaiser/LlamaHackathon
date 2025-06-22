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
        
        IMPORTANT: Return your response in valid JSON format with this structure:
        {
            "title": "Presentation Title",
            "sections": [
                {
                    "title": "Section Title",
                    "duration": 60,
                    "content": "Detailed content for this section...",
                    "demo_trigger": "trigger_name_or_null",
                    "visual_cue": "visual_element_or_null"
                }
            ],
            "total_duration": 300,
            "key_points": ["Point 1", "Point 2", "Point 3"],
            "demo_scenarios": ["Scenario 1", "Scenario 2"],
            "visual_elements": ["Visual 1", "Visual 2"]
        }
        
        Make the content specific to the provided codebase and requirements. Use the actual feature names, architecture details, and requirements from the context.
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
        Generate a compelling presentation script based on the following detailed context:
        
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
        
        INSTRUCTIONS:
        1. Use the ACTUAL feature names, architecture, and requirements from the context above
        2. Create sections that specifically address the documented requirements
        3. Reference the real codebase features and components
        4. Make demo scenarios based on the actual user flows and features
        5. Tailor the content to the specified audience and purpose
        6. Include specific timing that fits within the {request.duration} minute duration
        7. Create visual elements that would help explain the actual architecture and features
        
        Return your response in valid JSON format as specified in the system prompt.
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
        
        try:
            # First, try to extract JSON from the response
            import re
            
            # Look for JSON in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                parsed_response = json.loads(json_str)
                return parsed_response
            
            # If no JSON found, try to parse the response as markdown or text
            # and convert it to a structured format
            lines = response.strip().split('\n')
            sections = []
            current_section = None
            key_points = []
            demo_scenarios = []
            visual_elements = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Look for section headers
                if line.startswith('#') or line.upper() in ['INTRODUCTION', 'OVERVIEW', 'FEATURES', 'DEMO', 'CONCLUSION']:
                    if current_section:
                        sections.append(current_section)
                    
                    current_section = {
                        "title": line.lstrip('#').strip(),
                        "duration": 60,  # Default duration
                        "content": "",
                        "demo_trigger": None,
                        "visual_cue": None
                    }
                
                # Look for key points
                elif line.startswith('-') or line.startswith('*'):
                    key_points.append(line.lstrip('-* ').strip())
                
                # Look for demo scenarios
                elif 'demo' in line.lower() or 'scenario' in line.lower():
                    demo_scenarios.append(line.strip())
                
                # Look for visual elements
                elif any(word in line.lower() for word in ['diagram', 'chart', 'visual', 'image']):
                    visual_elements.append(line.strip())
                
                # Add content to current section
                elif current_section:
                    current_section["content"] += line + "\n"
            
            # Add the last section
            if current_section:
                sections.append(current_section)
            
            # If no sections found, create a default structure
            if not sections:
                sections = [
                    {
                        "title": "Introduction",
                        "duration": 60,
                        "content": response[:500] + "..." if len(response) > 500 else response,
                        "demo_trigger": None,
                        "visual_cue": None
                    }
                ]
            
            # Calculate total duration
            total_duration = sum(section.get("duration", 60) for section in sections)
            
            return {
                "title": "Generated Presentation",
                "sections": sections,
                "total_duration": total_duration,
                "key_points": key_points if key_points else ["Key point 1", "Key point 2", "Key point 3"],
                "demo_scenarios": demo_scenarios if demo_scenarios else ["Demo scenario 1", "Demo scenario 2"],
                "visual_elements": visual_elements if visual_elements else ["Visual element 1", "Visual element 2"],
                "raw_response": response  # Include the raw response for debugging
            }
            
        except Exception as e:
            # Fallback to structured format with raw response
            return {
                "title": "Generated Presentation",
                "sections": [
                    {
                        "title": "Presentation Content",
                        "duration": 300,
                        "content": response,
                        "demo_trigger": None,
                        "visual_cue": None
                    }
                ],
                "total_duration": 300,
                "key_points": ["Content generated successfully"],
                "demo_scenarios": ["Demo based on requirements"],
                "visual_elements": ["Visuals to be generated"],
                "raw_response": response,
                "parse_error": str(e)
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