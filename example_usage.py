"""
Example usage of Llama Maverick for presentation generation and agent orchestration
"""

import asyncio
import os
from src.core.llama_client import LlamaClient, LlamaConfig, CodebaseContext, DocumentContext
from src.core.synthesis_engine import SynthesisEngine, SynthesisInput
from config import LLAMA_API_KEY, LLAMA_BASE_URL, LLAMA_MODEL
import json

async def test_presentation_generation():
    """Test the complete presentation generation workflow"""
    
    # Configure Llama client
    config = LlamaConfig(
        api_key=LLAMA_API_KEY,
        base_url=LLAMA_BASE_URL,
        model=LLAMA_MODEL,
        max_tokens=4096,
        temperature=0.7
    )
    
    # Create client and synthesis engine
    llama_client = LlamaClient(config)
    synthesis_engine = SynthesisEngine(llama_client)
    
    try:
        # Mock codebase context (your partner's analysis will provide this)
        codebase_context = CodebaseContext(
            architecture="React + Node.js microservices",
            main_features=["User authentication", "Real-time chat", "File upload", "Dashboard analytics"],
            dependencies=["React", "Node.js", "MongoDB", "Socket.io", "AWS S3"],
            key_components=["AuthService", "ChatService", "FileService", "AnalyticsService"],
            user_flows=["User registration → Login → Dashboard → Chat → File sharing"]
        )
        
        # Mock document context (your document parser will provide this)
        document_context = DocumentContext(
            filename="requirements.pdf",
            requirements=[
                {
                    "title": "User Authentication System",
                    "description": "Secure user login and registration",
                    "priority": "High",
                    "features": ["Login form", "Registration", "Password reset"],
                    "acceptance_criteria": ["Users can register", "Users can login", "Passwords are encrypted"]
                },
                {
                    "title": "Real-time Chat Feature",
                    "description": "Instant messaging between users",
                    "priority": "High",
                    "features": ["Message sending", "Real-time updates", "Chat history"],
                    "acceptance_criteria": ["Messages send instantly", "Updates appear in real-time", "History is preserved"]
                }
            ],
            summary="High-priority features focused on user engagement and communication",
            total_requirements=2
        )
        
        # User prompt
        user_prompt = "Create a presentation for investors that showcases our innovative real-time collaboration platform. Focus on the technical architecture and user engagement features."
        
        # Presentation request
        presentation_request = {
            "purpose": "Investor pitch",
            "audience": "Technical investors",
            "duration": 10,  # minutes
            "focus_areas": ["Architecture", "User engagement", "Scalability"],
            "demo_requirements": ["Live chat demo", "User registration flow", "Dashboard overview"]
        }
        
        # Create synthesis input
        synthesis_input = SynthesisInput(
            codebase_context=codebase_context,
            document_context=document_context,
            user_prompt=user_prompt
        )
        
        print("🚀 Starting Presentation Generation...")
        print("=" * 60)
        print(f"📝 User Prompt: {user_prompt}")
        print(f"🎯 Purpose: {presentation_request['purpose']}")
        print(f"👥 Audience: {presentation_request['audience']}")
        print(f"⏱️ Duration: {presentation_request['duration']} minutes")
        print("=" * 60)
        
        # Generate presentation and agent plan
        result = await synthesis_engine.synthesize_and_generate(
            synthesis_input, presentation_request
        )
        
        print("\n✅ Generation Complete!")
        print("=" * 60)
        print(f"📊 Summary: {result.summary}")
        print("\n🎤 Presentation Script:")
        print(f"   Title: {result.presentation_script.get('title', 'N/A')}")
        print(f"   Duration: {result.presentation_script.get('total_duration', 0)} seconds")
        print(f"   Sections: {len(result.presentation_script.get('sections', []))}")
        print(f"   Key Points: {len(result.presentation_script.get('key_points', []))}")
        
        print("\n🤖 Agent Execution Plan:")
        print(f"   Agents Required: {result.agent_execution_plan.get('agents_required', [])}")
        print(f"   Execution Steps: {len(result.agent_execution_plan.get('execution_sequence', []))}")
        print(f"   Demo Scenarios: {len(result.agent_execution_plan.get('demo_scenarios', []))}")
        
        print("\n📋 Detailed Output:")
        print("-" * 40)
        print("Presentation Script:")
        print(json.dumps(result.presentation_script, indent=2))
        print("\nAgent Execution Plan:")
        print(json.dumps(result.agent_execution_plan, indent=2))
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await llama_client.close()

async def test_llama_maverick_basic():
    """Test basic Llama Maverick functionality"""
    
    config = LlamaConfig(
        api_key=LLAMA_API_KEY,
        base_url=LLAMA_BASE_URL,
        model=LLAMA_MODEL,
        max_tokens=2048,
        temperature=0.7
    )
    
    client = LlamaClient(config)
    
    try:
        prompt = "Explain the key benefits of using Llama 4 Maverick for presentation generation in 3 bullet points."
        
        print("🤖 Testing Llama 4 Maverick Basic...")
        print(f"📝 Prompt: {prompt}")
        print("-" * 50)
        
        response = await client._call_llama(prompt)
        
        print("✅ Response:")
        print(response)
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    print("🚀 Llama 4 Maverick Presentation Generation Test Suite")
    print("=" * 70)
    
    # Test basic functionality first
    print("\n1️⃣ Testing Basic Llama Maverick...")
    asyncio.run(test_llama_maverick_basic())
    
    print("\n" + "=" * 70)
    
    # Test complete workflow
    print("\n2️⃣ Testing Complete Presentation Generation...")
    asyncio.run(test_presentation_generation())
    
    print("\n✅ All tests completed!") 