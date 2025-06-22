#!/usr/bin/env python3
"""
Test Avatar Integration - Demonstrates synchronized avatar presentations with demo coordination
"""

import os
import sys
import json
from datetime import datetime
import asyncio

# Add src to path
sys.path.append('src')

from core.unified_processor import UnifiedProcessor
from core.tavus_avatar_controller import TavusAvatarController

async def test_avatar_integration():
    """Test the complete avatar integration pipeline"""
    
    print("🚀 Testing Avatar Integration Pipeline")
    print("=" * 60)
    
    # Test configuration
    github_repo = "https://github.com/cyclotruc/gitingest"
    pdf_path = "Calculator_Requirements_Doc.pdf"
    demo_duration = 7
    audience = "Mixed Technical & Business"
    purpose = "Technical Deep Dive"
    focus_areas = ["Backend Architecture", "API Integration", "User Interface & UX", "Security Features"]
    
    print(f"📊 Test Configuration:")
    print(f"   GitHub Repo: {github_repo}")
    print(f"   PDF Document: {pdf_path}")
    print(f"   Demo Duration: {demo_duration} minutes")
    print(f"   Audience: {audience}")
    print(f"   Purpose: {purpose}")
    print(f"   Focus Areas: {', '.join(focus_areas)}")
    print()
    
    try:
        # Initialize processor
        processor = UnifiedProcessor()
        
        print("🔄 Processing complete request with avatar integration...")
        
        # Prepare UI preferences
        ui_preferences = {
            "demo_duration": demo_duration,
            "audience_type": audience,
            "demo_purpose": purpose,
            "focus_areas": focus_areas
        }
        # Process the request
        result = await processor.process_complete_request(
            github_url=github_repo,
            pdf_file_path=pdf_path,
            ui_preferences=ui_preferences
        )
        
        # Extract avatar presentation
        avatar_presentation = getattr(result, 'avatar_presentation', {})
        
        print("✅ Processing complete!")
        print()
        
        # Display avatar integration results
        print("🤖 AVATAR INTEGRATION RESULTS")
        print("=" * 50)
        
        # Avatar script details
        avatar_script = avatar_presentation.get('avatar_script', {})
        presentation = avatar_script.get('presentation', {})
        segments = presentation.get('segments', [])
        
        print(f"📝 Presentation Title: {presentation.get('title', 'N/A')}")
        print(f"📊 Total Segments: {len(segments)}")
        print(f"⏱️  Total Duration: {avatar_presentation.get('metadata', {}).get('total_duration', 0):.1f} seconds")
        print(f"🎯 Demo Actions: {avatar_presentation.get('metadata', {}).get('demo_actions_count', 0)}")
        print(f"📋 Status: {avatar_presentation.get('status', 'unknown')}")
        print()
        
        # Show coordinated segments
        print("🎭 COORDINATED PRESENTATION SEGMENTS")
        print("-" * 40)
        
        for i, segment in enumerate(segments, 1):
            segment_id = segment.get('id', f'segment_{i}')
            text = segment.get('text', 'No text')
            duration = segment.get('duration', 0)
            start_time = segment.get('start_time', 0)
            
            print(f"Segment {i}:")
            print(f"  ID: {segment_id}")
            print(f"  Start Time: {start_time:.1f}s")
            print(f"  Duration: {duration:.1f}s")
            print(f"  Text: {text[:100]}{'...' if len(text) > 100 else ''}")
            
            # Check for demo coordination
            demo_coordination = avatar_script.get('demo_coordination', {})
            if segment_id in demo_coordination:
                demo_info = demo_coordination[segment_id]
                print(f"  🎯 DEMO COORDINATION:")
                print(f"    Action ID: {demo_info.get('action_id', 'N/A')}")
                print(f"    Gesture: {demo_info.get('gesture', 'N/A')}")
                print(f"    Completion Signal: {demo_info.get('completion_signal', 'N/A')}")
                print(f"    Pause Duration: {demo_info.get('pause_duration', 0):.1f}s")
            
            print()
        
        # Show demo coordination details
        demo_coordination = avatar_presentation.get('demo_coordination', {})
        if demo_coordination:
            print("🎯 DEMO COORDINATION DETAILS")
            print("-" * 30)
            
            for segment_id, coordination in demo_coordination.items():
                print(f"Segment: {segment_id}")
                print(f"  Action: {coordination.get('action_id', 'N/A')}")
                print(f"  Signal: {coordination.get('completion_signal', 'N/A')}")
                print(f"  Gesture: {coordination.get('gesture', 'N/A')}")
                print()
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"test_outputs/avatar_integration_test_{timestamp}.txt"
        
        os.makedirs("test_outputs", exist_ok=True)
        
        with open(output_file, "w") as f:
            f.write("=" * 80 + "\n")
            f.write("AVATAR INTEGRATION TEST RESULTS\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"GitHub Repo: {github_repo}\n")
            f.write(f"PDF Document: {pdf_path}\n")
            f.write(f"Demo Duration: {demo_duration} minutes\n")
            f.write(f"Audience: {audience}\n")
            f.write(f"Purpose: {purpose}\n")
            f.write(f"Focus Areas: {', '.join(focus_areas)}\n\n")
            
            f.write("=" * 50 + "\n")
            f.write("AVATAR PRESENTATION SCRIPT\n")
            f.write("=" * 50 + "\n")
            f.write(json.dumps(avatar_presentation, indent=2))
            f.write("\n\n")
            
            f.write("=" * 50 + "\n")
            f.write("COORDINATION SCRIPT\n")
            f.write("=" * 50 + "\n")
            f.write(avatar_presentation.get('coordination_script', 'No coordination script generated'))
            f.write("\n\n")
        
        print(f"✅ Results saved to: {output_file}")
        
        # Show file size
        file_size = os.path.getsize(output_file) / 1024  # KB
        print(f"📄 File size: {file_size:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during avatar integration test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_avatar_controller_directly():
    """Test the Tavus avatar controller directly"""
    
    print("\n🎭 Testing Tavus Avatar Controller Directly")
    print("=" * 50)
    
    # Create sample presentation script and execution plan
    presentation_script = {
        "presentation_script": {
            "sections": [
                {
                    "title": "Introduction",
                    "duration": 30,
                    "content": "Welcome to our AI-powered demo. Let me show you how our system works by demonstrating the key features.",
                    "demo_steps": ["Open the application", "Navigate to the main dashboard"]
                },
                {
                    "title": "Feature Demonstration",
                    "duration": 60,
                    "content": "Now let's explore the core functionality. I'll show you how the system processes requirements and generates presentations.",
                    "demo_steps": ["Upload requirements document", "Analyze codebase", "Generate presentation script"]
                }
            ]
        }
    }
    
    execution_plan = {
        "demo_plan": {
            "automation_steps": [
                "Click on the login button",
                "Enter credentials and submit",
                "Navigate to the dashboard",
                "Upload a PDF document",
                "Click the analyze button",
                "Wait for processing to complete",
                "Review the generated presentation"
            ]
        }
    }
    
    try:
        # Initialize avatar controller (with dummy API key for testing)
        controller = TavusAvatarController("dummy_api_key")
        
        # Synthesize avatar script
        avatar_script = controller.synthesize_avatar_script(presentation_script, execution_plan)
        
        print("✅ Avatar script synthesis successful!")
        print(f"📊 Total duration: {avatar_script.get('metadata', {}).get('total_duration', 0):.1f} seconds")
        print(f"🎯 Demo actions: {avatar_script.get('metadata', {}).get('demo_actions_count', 0)}")
        print(f"📋 Sections: {avatar_script.get('metadata', {}).get('sections_count', 0)}")
        
        # Show timeline
        timeline = avatar_script.get('timeline', [])
        print(f"\n📅 Timeline with {len(timeline)} segments:")
        
        for i, segment in enumerate(timeline, 1):
            print(f"  {i}. {segment.start_time:.1f}s - {segment.start_time + segment.duration:.1f}s: {segment.text[:50]}...")
            if segment.pause_for_demo:
                print(f"     🎯 DEMO: {segment.demo_action} (gesture: {segment.gesture})")
        
        # Generate coordination script
        coordination_script = controller.generate_coordination_script(avatar_script)
        
        print(f"\n🤖 Generated coordination script ({len(coordination_script.split(chr(10)))} lines)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing avatar controller: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Llama Hackathon Demo Generator - Avatar Integration Test")
    print("=" * 70)
    
    # Test 1: Complete integration
    success1 = asyncio.run(test_avatar_integration())
    
    # Test 2: Direct controller test
    success2 = test_avatar_controller_directly()
    
    print("\n" + "=" * 70)
    print("🎯 TEST SUMMARY")
    print("=" * 70)
    print(f"✅ Complete Integration Test: {'PASSED' if success1 else 'FAILED'}")
    print(f"✅ Direct Controller Test: {'PASSED' if success2 else 'FAILED'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! Avatar integration is working correctly.")
        print("🚀 Ready for synchronized avatar presentations with demo coordination!")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.") 