"""
Complete Pipeline Test - Validate Llama's ability to generate presentations
with GitHub repo, PDF requirements, and UI preferences
"""

import asyncio
import os
import json
from datetime import datetime
from pathlib import Path
from src.core.unified_processor import UnifiedProcessor

async def test_complete_pipeline():
    """Test the complete pipeline with real inputs and save output to file"""
    
    # Get API key from environment
    api_key = os.getenv("LLAMA_API_KEY")
    if not api_key:
        print("❌ LLAMA_API_KEY not found in environment")
        return
    
    print("🚀 Testing Complete Pipeline")
    print("=" * 50)
    
    # Initialize processor
    processor = UnifiedProcessor(api_key)
    
    # Test inputs (simulating UI inputs)
    test_inputs = {
        "github_url": "https://github.com/cyclotruc/gitingest",
        "pdf_file_path": "Calculator_Requirements_Doc.pdf",
        "ui_preferences": {
            "demo_duration": 1,  # 1 minute to conserve Tavus credits
            "audience_type": "Mixed Technical & Business",
            "demo_purpose": "Technical Deep Dive",
            "focus_areas": [
                "Backend Architecture", 
                "API Integration", 
                "User Interface & UX",
                "Security Features"
            ],
            "include_code_analysis": True,
            "include_risk_assessment": True
        }
    }
    
    print(f"📊 Test Configuration:")
    print(f"   GitHub Repo: {test_inputs['github_url']}")
    print(f"   PDF Document: {test_inputs['pdf_file_path']}")
    print(f"   Demo Duration: {test_inputs['ui_preferences']['demo_duration']} minutes")
    print(f"   Audience: {test_inputs['ui_preferences']['audience_type']}")
    print(f"   Purpose: {test_inputs['ui_preferences']['demo_purpose']}")
    print(f"   Focus Areas: {', '.join(test_inputs['ui_preferences']['focus_areas'])}")
    
    try:
        print("\n🔄 Processing complete request...")
        
        # Process the complete request
        result = await processor.process_complete_request(
            github_url=test_inputs["github_url"],
            pdf_file_path=test_inputs["pdf_file_path"],
            ui_preferences=test_inputs["ui_preferences"]
        )
        
        print("✅ Processing complete!")
        
        # Save results to file in the output directory
        output_dir = "test_outputs"
        os.makedirs(output_dir, exist_ok=True)
        output_filename = os.path.join(output_dir, f"pipeline_test_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("LLAMA HACKATHON DEMO GENERATOR - COMPLETE PIPELINE TEST\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"GitHub Repo: {test_inputs['github_url']}\n")
            f.write(f"PDF Document: {test_inputs['pdf_file_path']}\n")
            f.write(f"Demo Duration: {test_inputs['ui_preferences']['demo_duration']} minutes\n")
            f.write(f"Audience: {test_inputs['ui_preferences']['audience_type']}\n")
            f.write(f"Purpose: {test_inputs['ui_preferences']['demo_purpose']}\n")
            f.write(f"Focus Areas: {', '.join(test_inputs['ui_preferences']['focus_areas'])}\n\n")
            
            # 1. Codebase Analysis
            f.write("=" * 50 + "\n")
            f.write("1. CODEBASE ANALYSIS\n")
            f.write("=" * 50 + "\n")
            f.write(f"Architecture: {result.codebase_context.architecture}\n")
            f.write(f"Main Features: {', '.join(result.codebase_context.main_features)}\n")
            f.write(f"Dependencies: {', '.join(result.codebase_context.dependencies)}\n")
            f.write(f"Key Components: {', '.join(result.codebase_context.key_components)}\n")
            f.write(f"User Flows: {', '.join(result.codebase_context.user_flows)}\n\n")
            
            # 2. Requirements Analysis
            f.write("=" * 50 + "\n")
            f.write("2. REQUIREMENTS ANALYSIS\n")
            f.write("=" * 50 + "\n")
            f.write(f"Document: {result.document_context.filename}\n")
            f.write(f"Total Requirements: {result.document_context.total_requirements}\n")
            f.write(f"Summary: {result.document_context.summary}\n\n")
            
            f.write("Requirements Details:\n")
            for i, req in enumerate(result.document_context.requirements, 1):
                f.write(f"\nRequirement {i}:\n")
                f.write(f"  Title: {req.get('title', 'N/A')}\n")
                f.write(f"  Priority: {req.get('priority', 'N/A')}\n")
                f.write(f"  Description: {req.get('description', 'N/A')[:200]}...\n")
                f.write(f"  Features: {', '.join(req.get('features', []))}\n")
                f.write(f"  Acceptance Criteria: {', '.join(req.get('acceptance_criteria', []))}\n")
            
            # 3. Holistic Context
            f.write("\n" + "=" * 50 + "\n")
            f.write("3. HOLISTIC CONTEXT (Sent to Llama)\n")
            f.write("=" * 50 + "\n")
            f.write(result.holistic_context)
            f.write("\n\n")
            
            # 4. Generated Presentation Script
            f.write("=" * 50 + "\n")
            f.write("4. GENERATED PRESENTATION SCRIPT\n")
            f.write("=" * 50 + "\n")
            
            if isinstance(result.presentation_script, dict):
                if "presentation_script" in result.presentation_script:
                    script = result.presentation_script["presentation_script"]
                    f.write(f"Total Duration: {script.get('total_duration', 'N/A')} seconds\n\n")
                    
                    if "sections" in script:
                        for i, section in enumerate(script["sections"], 1):
                            f.write(f"Section {i}: {section.get('title', 'Untitled')}\n")
                            f.write(f"Duration: {section.get('duration', 0)} seconds\n")
                            f.write(f"Content:\n{section.get('content', 'No content')}\n")
                            
                            if section.get('demo_steps'):
                                f.write(f"Demo Steps:\n")
                                for step in section['demo_steps']:
                                    f.write(f"  - {step}\n")
                            
                            f.write("\n" + "-" * 30 + "\n\n")
                    else:
                        f.write(json.dumps(script, indent=2))
                else:
                    f.write(json.dumps(result.presentation_script, indent=2))
            else:
                f.write(str(result.presentation_script))
            
            # 5. Agent Execution Plan
            f.write("\n" + "=" * 50 + "\n")
            f.write("5. AGENT EXECUTION PLAN\n")
            f.write("=" * 50 + "\n")
            f.write(json.dumps(result.agent_execution_plan, indent=2))
            f.write("\n\n")
            
            # 6. Analysis Summary
            f.write("=" * 50 + "\n")
            f.write("6. ANALYSIS SUMMARY\n")
            f.write("=" * 50 + "\n")
            f.write(json.dumps(result.analysis_summary, indent=2))
            f.write("\n\n")
            
            # 7. Validation Notes
            f.write("=" * 50 + "\n")
            f.write("7. VALIDATION NOTES\n")
            f.write("=" * 50 + "\n")
            f.write("✅ What to check:\n")
            f.write("1. Does the presentation follow the 6-section structure?\n")
            f.write("2. Are demo steps specific and actionable?\n")
            f.write("3. Does it adapt to the specified audience and duration?\n")
            f.write("4. Are technical and business aspects balanced?\n")
            f.write("5. Does the agent execution plan include automation steps?\n")
            f.write("6. Is the content relevant to both codebase and requirements?\n")
            f.write("7. Are timing constraints respected?\n")
            f.write("8. Does it highlight innovation and hackathon appeal?\n\n")
            
            f.write("🎯 Expected Quality Indicators:\n")
            f.write("- Clear narrative flow from problem to solution\n")
            f.write("- Specific demo instructions with UI selectors\n")
            f.write("- Balanced technical and business content\n")
            f.write("- Engaging and professional tone\n")
            f.write("- Hackathon-appropriate innovation focus\n")
            f.write("- Automation-ready demo steps\n")
        
        print(f"✅ Results saved to: {output_filename}")
        print(f"📄 File size: {Path(output_filename).stat().st_size / 1024:.1f} KB")
        
        # Show quick summary
        print(f"\n📊 Quick Summary:")
        print(f"   Codebase Features: {len(result.codebase_context.main_features)}")
        print(f"   Requirements: {result.document_context.total_requirements}")
        print(f"   Presentation Sections: {len(result.presentation_script.get('presentation_script', {}).get('sections', []))}")
        print(f"   Agent Plan: {len(result.agent_execution_plan.get('agents_required', []))} agents")
        
        return output_filename
        
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        return None

async def test_multiple_scenarios():
    """Test different scenarios to validate flexibility"""
    
    api_key = os.getenv("LLAMA_API_KEY")
    if not api_key:
        print("❌ LLAMA_API_KEY not found in environment")
        return
    
    processor = UnifiedProcessor(api_key)
    
    scenarios = [
        {
            "name": "Technical Deep Dive",
            "github_url": "https://github.com/cyclotruc/gitingest",
            "ui_preferences": {
                "demo_duration": 1,
                "audience_type": "Technical Developers",
                "demo_purpose": "Technical Deep Dive",
                "focus_areas": ["Backend Architecture", "API Integration"]
            }
        },
        {
            "name": "Business Pitch",
            "github_url": "https://github.com/cyclotruc/gitingest",
            "ui_preferences": {
                "demo_duration": 1,
                "audience_type": "Business Stakeholders",
                "demo_purpose": "Investor Pitch",
                "focus_areas": ["Business Value", "Market Potential"]
            }
        }
    ]
    
    print("\n🔄 Testing Multiple Scenarios...")
    
    for scenario in scenarios:
        print(f"\n📋 Testing: {scenario['name']}")
        try:
            result = await processor.process_complete_request(
                github_url=scenario["github_url"],
                ui_preferences=scenario["ui_preferences"]
            )
            print(f"✅ {scenario['name']}: {len(result.presentation_script.get('presentation_script', {}).get('sections', []))} sections")
        except Exception as e:
            print(f"❌ {scenario['name']}: {e}")

if __name__ == "__main__":
    print("🚀 Llama Hackathon Demo Generator - Complete Pipeline Validation")
    print("=" * 70)
    
    # Run main test
    output_file = asyncio.run(test_complete_pipeline())
    
    if output_file:
        print(f"\n🎉 Pipeline validation complete!")
        print(f"📄 Review the output in: {output_file}")
        print(f"🔍 Check that Llama generated:")
        print(f"   - Structured presentation with proper sections")
        print(f"   - Specific demo automation steps")
        print(f"   - Audience-appropriate content")
        print(f"   - Technical and business balance")
        print(f"   - Hackathon-appropriate innovation focus")
        
        # Run additional scenarios
        asyncio.run(test_multiple_scenarios())
    else:
        print("❌ Pipeline validation failed!") 