#!/usr/bin/env python3
"""
Unified Processor - Combines all inputs and generates demo content
"""

import os
import json
import asyncio
from typing import Dict, Any, Optional, List
from pathlib import Path

from src.analysis.document_parser import DocumentParser
from .github_analyzer import GitHubAnalyzer
from .synthesis_engine import SynthesisEngine
from .llama_client import LlamaClient, LlamaConfig
from .simple_avatar_presenter import SimpleAvatarPresenter
from config import SYSTEM_PROMPT

class UnifiedProcessor:
    """Unified processor that combines all inputs and generates demo content"""
    
    def __init__(self):
        self.document_parser = DocumentParser()
        self.github_analyzer = GitHubAnalyzer()
        
        # Initialize Llama client
        api_key = os.getenv("LLAMA_API_KEY")
        if not api_key:
            raise ValueError("LLAMA_API_KEY environment variable is required")
        
        llama_config = LlamaConfig(api_key=api_key)
        self.llama_client = LlamaClient(llama_config)
        
        # Initialize synthesis engine with llama client
        self.synthesis_engine = SynthesisEngine(self.llama_client)
        self.avatar_presenter = SimpleAvatarPresenter()
        
    async def process_demo_request(
        self,
        github_url: Optional[str] = None,
        requirements_file = None,
        requirements_path: Optional[str] = None,
        audience: str = "Mixed Technical & Business",
        purpose: str = "Feature Showcase",
        demo_duration: int = 5
    ) -> Dict[str, Any]:
        """Process demo request and generate all content"""
        
        print("🚀 Starting unified demo processing...")
        
        # Step 1: Parse requirements document
        requirements_data = self._parse_requirements(requirements_file, requirements_path)
        
        # Step 2: Analyze GitHub repository
        github_data = self._analyze_github(github_url)
        
        # Step 3: Generate presentation script
        presentation_script = await self._generate_presentation_script(
            requirements_data, github_data, audience, purpose, demo_duration
        )
        
        # Step 4: Generate demo plan
        demo_plan = self._generate_demo_plan(
            requirements_data, github_data, demo_duration
        )
        
        # Step 5: Generate avatar script
        avatar_script = self._generate_avatar_script(
            presentation_script, demo_plan
        )
        
        # Step 6: Compile results
        results = {
            "presentation_script": presentation_script,
            "demo_plan": demo_plan,
            "avatar_script": avatar_script,
            "requirements_summary": self._summarize_requirements(requirements_data),
            "github_summary": self._summarize_github(github_data),
            "processing_metadata": {
                "audience": audience,
                "purpose": purpose,
                "demo_duration": demo_duration,
                "total_requirements": len(requirements_data) if requirements_data else 0,
                "github_analyzed": github_url is not None
            }
        }
        
        print("✅ Demo processing completed successfully!")
        return results
    
    def _parse_requirements(self, requirements_file, requirements_path: Optional[str]) -> List[Dict[str, Any]]:
        """Parse requirements document"""
        
        if requirements_file:
            print("📄 Parsing uploaded requirements file...")
            # Handle uploaded file
            temp_path = "temp_requirements.pdf"
            with open(temp_path, "wb") as f:
                f.write(requirements_file.getbuffer())
            
            parsed_doc = self.document_parser.parse_document(temp_path)
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
        elif requirements_path:
            print(f"📄 Parsing requirements from: {requirements_path}")
            parsed_doc = self.document_parser.parse_document(requirements_path)
        else:
            print("⚠️ No requirements document provided")
            parsed_doc = None
        
        # Convert ParsedDocument to list of requirement dictionaries
        if parsed_doc and hasattr(parsed_doc, 'requirements'):
            requirements_data = []
            for req in parsed_doc.requirements:
                req_dict = {
                    'title': req.title,
                    'description': req.description,
                    'priority': req.priority,
                    'features': req.features,
                    'acceptance_criteria': req.acceptance_criteria,
                    'technical_notes': req.technical_notes,
                    'page_number': req.page_number
                }
                requirements_data.append(req_dict)
        else:
            requirements_data = []
        
        print(f"📋 Extracted {len(requirements_data)} requirements")
        return requirements_data
    
    def _analyze_github(self, github_url: Optional[str]) -> Dict[str, Any]:
        """Analyze GitHub repository"""
        
        if github_url:
            print(f"🔍 Analyzing GitHub repository: {github_url}")
            github_data = self.github_analyzer.analyze_repository(github_url)
        else:
            print("⚠️ No GitHub URL provided")
            github_data = {
                "repository_info": {"name": "demo-app", "description": "Sample application"},
                "codebase_summary": "Modern web application with key features",
                "key_features": ["User authentication", "Dashboard", "API endpoints"],
                "architecture": "Microservices architecture",
                "tech_stack": ["Python", "React", "PostgreSQL"]
            }
        
        return github_data
    
    async def _generate_presentation_script(
        self,
        requirements_data: List[Dict[str, Any]],
        github_data: Dict[str, Any],
        audience: str,
        purpose: str,
        demo_duration: int
    ) -> str:
        """Generate presentation script using Llama 4"""
        
        print("🤖 Generating presentation script with Llama 4...")
        
        # Convert data to the expected format for LlamaClient
        from .llama_client import CodebaseContext, DocumentContext, PresentationRequest
        
        # Create CodebaseContext
        codebase_context = CodebaseContext(
            architecture=github_data.get('architecture', 'Unknown'),
            main_features=github_data.get('key_features', []),
            dependencies=github_data.get('tech_stack', []),
            key_components=github_data.get('key_features', []),
            user_flows=github_data.get('key_features', [])
        )
        
        # Create DocumentContext
        document_context = DocumentContext(
            filename="requirements.pdf",
            requirements=requirements_data,
            summary=f"Requirements document with {len(requirements_data)} features",
            total_requirements=len(requirements_data)
        )
        
        # Create PresentationRequest
        presentation_request = PresentationRequest(
            purpose=purpose,
            audience=audience,
            duration=demo_duration,
            focus_areas=github_data.get('key_features', []),
            demo_requirements=[req.get('title', 'Feature') for req in requirements_data]
        )
        
        # Generate script using LlamaClient directly
        user_prompt = f"Create a compelling presentation for {audience} about {purpose} with {demo_duration} minutes duration"
        
        script_result = await self.llama_client.generate_presentation_script(
            codebase_context=codebase_context,
            document_context=document_context,
            user_prompt=user_prompt,
            request=presentation_request
        )
        
        # Convert to string if it's a dict
        if isinstance(script_result, dict):
            script = json.dumps(script_result, indent=2)
        else:
            script = str(script_result)
        
        print(f"📝 Generated script: {len(script)} characters")
        return script
    
    def _generate_demo_plan(
        self,
        requirements_data: List[Dict[str, Any]],
        github_data: Dict[str, Any],
        demo_duration: int
    ) -> Dict[str, Any]:
        """Generate demo execution plan"""
        
        print("📋 Generating demo execution plan...")
        
        # Create demo steps based on requirements
        demo_steps = []
        
        if requirements_data:
            for i, req in enumerate(requirements_data[:3]):  # Limit to 3 main features
                step = {
                    "step_id": f"step_{i+1}",
                    "action": f"Demonstrate {req.get('title', 'Feature')}",
                    "description": req.get('description', 'Show key functionality'),
                    "duration": demo_duration * 60 // len(requirements_data[:3]),  # Distribute time
                    "expected_outcome": f"Successfully showcase {req.get('title', 'feature')}",
                    "requirements": req
                }
                demo_steps.append(step)
        else:
            # Fallback demo steps
            demo_steps = [
                {
                    "step_id": "step_1",
                    "action": "Navigate to application",
                    "description": "Open the main application interface",
                    "duration": 30,
                    "expected_outcome": "Application loads successfully"
                },
                {
                    "step_id": "step_2", 
                    "action": "Show key features",
                    "description": "Demonstrate main functionality",
                    "duration": demo_duration * 60 - 30,
                    "expected_outcome": "Features work as expected"
                }
            ]
        
        demo_plan = {
            "demo_url": "https://demo.example.com",  # Placeholder
            "estimated_duration": demo_duration,
            "steps": demo_steps,
            "prerequisites": ["Working internet connection", "Modern web browser"],
            "success_criteria": ["All features demonstrated", "Smooth user experience"]
        }
        
        print(f"📋 Generated {len(demo_steps)} demo steps")
        return demo_plan
    
    def _generate_avatar_script(
        self,
        presentation_script: str,
        demo_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate avatar script for Tavus"""
        
        print("🎭 Generating avatar script...")
        
        # Load script into avatar presenter
        self.avatar_presenter.load_script(presentation_script, demo_plan)
        
        # Generate avatar script
        avatar_script = self.avatar_presenter.generate_avatar_script()
        
        print(f"🎭 Generated avatar script with {len(avatar_script['presentation']['segments'])} segments")
        return avatar_script
    
    def _prepare_llama_context(
        self,
        requirements_data: List[Dict[str, Any]],
        github_data: Dict[str, Any],
        audience: str,
        purpose: str,
        demo_duration: int
    ) -> Dict[str, Any]:
        """Prepare context for Llama 4"""
        
        context = {
            "requirements": requirements_data,
            "github_analysis": github_data,
            "audience": audience,
            "purpose": purpose,
            "demo_duration": demo_duration,
            "system_prompt": SYSTEM_PROMPT
        }
        
        return context
    
    def _summarize_requirements(self, requirements_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Summarize requirements data"""
        
        if not requirements_data:
            return {"count": 0, "features": []}
        
        features = [req.get('title', 'Unknown') for req in requirements_data]
        priorities = [req.get('priority', 'Medium') for req in requirements_data]
        
        return {
            "count": len(requirements_data),
            "features": features,
            "priorities": priorities,
            "high_priority_count": sum(1 for p in priorities if p.lower() == 'high'),
            "total_pages": max([req.get('page_number', 0) for req in requirements_data], default=0)
        }
    
    def _summarize_github(self, github_data: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize GitHub analysis"""
        
        return {
            "repository_name": github_data.get('repository_info', {}).get('name', 'Unknown'),
            "language": github_data.get('repository_info', {}).get('language', 'Unknown'),
            "key_features": github_data.get('key_features', []),
            "tech_stack": github_data.get('tech_stack', []),
            "architecture": github_data.get('architecture', 'Unknown')
        }
    
    def save_results(self, results: Dict[str, Any], output_dir: str = "output"):
        """Save processing results to files"""
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Save presentation script
        with open(f"{output_dir}/presentation_script.txt", "w") as f:
            f.write(results["presentation_script"])
        
        # Save demo plan
        with open(f"{output_dir}/demo_plan.json", "w") as f:
            json.dump(results["demo_plan"], f, indent=2)
        
        # Save avatar script
        with open(f"{output_dir}/avatar_script.json", "w") as f:
            json.dump(results["avatar_script"], f, indent=2)
        
        # Save complete results
        with open(f"{output_dir}/complete_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Results saved to {output_dir}/")

# Example usage
if __name__ == "__main__":
    processor = UnifiedProcessor()
    
    # Test with sample data
    result = processor.process_demo_request(
        github_url="https://github.com/example/demo-app",
        requirements_path="sample_requirements.pdf",
        audience="Mixed Technical & Business",
        purpose="Feature Showcase",
        demo_duration=5
    )
    
    print("✅ Processing completed!")
    print(f"📝 Script length: {len(result['presentation_script'])} chars")
    print(f"📋 Demo steps: {len(result['demo_plan']['steps'])}")
    print(f"🎭 Avatar segments: {len(result['avatar_script']['presentation']['segments'])}") 