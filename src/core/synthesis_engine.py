"""
Synthesis Engine - Combines codebase analysis, document parsing, and user prompt for Llama processing
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from src.analysis.document_parser import ParsedDocument
from src.core.llama_client import CodebaseContext, DocumentContext

@dataclass
class SynthesisInput:
    """Input data for synthesis"""
    codebase_context: CodebaseContext
    document_context: DocumentContext
    user_prompt: str

@dataclass
class SynthesisOutput:
    """Output from synthesis process"""
    presentation_script: Dict[str, Any]
    agent_execution_plan: Dict[str, Any]
    summary: str

class SynthesisEngine:
    """Engine for synthesizing inputs and generating presentation outputs"""
    
    def __init__(self, llama_client):
        self.llama_client = llama_client
    
    async def synthesize_and_generate(
        self, 
        synthesis_input: SynthesisInput,
        presentation_request: Dict[str, Any]
    ) -> SynthesisOutput:
        """Main synthesis and generation process"""
        
        # Step 1: Generate presentation script
        presentation_script = await self.llama_client.generate_presentation_script(
            codebase_context=synthesis_input.codebase_context,
            document_context=synthesis_input.document_context,
            user_prompt=synthesis_input.user_prompt,
            request=presentation_request
        )
        
        # Step 2: Generate agent execution plan
        agent_execution_plan = await self.llama_client.generate_agent_execution_plan(
            codebase_context=synthesis_input.codebase_context,
            document_context=synthesis_input.document_context,
            user_prompt=synthesis_input.user_prompt,
            presentation_script=presentation_script
        )
        
        # Step 3: Generate summary
        summary = self._generate_synthesis_summary(synthesis_input, presentation_script, agent_execution_plan)
        
        return SynthesisOutput(
            presentation_script=presentation_script,
            agent_execution_plan=agent_execution_plan,
            summary=summary
        )
    
    def _generate_synthesis_summary(
        self, 
        synthesis_input: SynthesisInput,
        presentation_script: Dict[str, Any],
        agent_execution_plan: Dict[str, Any]
    ) -> str:
        """Generate human-readable summary of the synthesis"""
        
        summary_parts = [
            f"🎯 Synthesis Complete",
            f"📁 Codebase: {len(synthesis_input.codebase_context.main_features)} features",
            f"📄 Document: {synthesis_input.document_context.filename} ({synthesis_input.document_context.total_requirements} requirements)",
            f"🎤 Presentation: {presentation_script.get('total_duration', 0)} seconds",
            f"🤖 Agents: {len(agent_execution_plan.get('agents_required', []))} required",
            f"🎬 Demos: {len(agent_execution_plan.get('demo_scenarios', []))} scenarios"
        ]
        
        return " | ".join(summary_parts)
    
    def prepare_llama_context(self, synthesis_input: SynthesisInput) -> str:
        """Prepare comprehensive context for Llama processing"""
        
        context_parts = [
            "=== USER PROMPT ===",
            synthesis_input.user_prompt,
            "",
            "=== CODEBASE ANALYSIS ===",
            f"Architecture: {synthesis_input.codebase_context.architecture}",
            f"Main Features: {', '.join(synthesis_input.codebase_context.main_features)}",
            f"Dependencies: {', '.join(synthesis_input.codebase_context.dependencies)}",
            f"Key Components: {', '.join(synthesis_input.codebase_context.key_components)}",
            f"User Flows: {', '.join(synthesis_input.codebase_context.user_flows)}",
            "",
            "=== REQUIREMENTS DOCUMENT ===",
            f"Document: {synthesis_input.document_context.filename}",
            f"Summary: {synthesis_input.document_context.summary}",
            f"Total Requirements: {synthesis_input.document_context.total_requirements}",
            "",
            "=== REQUIREMENTS DETAILS ===",
            json.dumps(synthesis_input.document_context.requirements, indent=2)
        ]
        
        return "\n".join(context_parts) 