#!/usr/bin/env python3
"""
Test Simple Avatar Integration - Validates avatar presentation without browser automation
"""

import json
import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.unified_processor import UnifiedProcessor
from core.simple_avatar_presenter import SimpleAvatarPresenter

def test_simple_avatar_integration():
    """Test the simple avatar integration flow"""
    
    print("🎭 Testing Simple Avatar Integration")
    print("=" * 50)
    
    # Test data
    test_data = {
        "github_url": "https://github.com/example/demo-app",
        "requirements_path": "sample_requirements.pdf",
        "audience": "Mixed Technical & Business",
        "purpose": "Feature Showcase",
        "demo_duration": 1
    }
    
    # Step 1: Test Unified Processor
    print("\n1️⃣ Testing Unified Processor...")
    try:
        processor = UnifiedProcessor()
        
        # Process demo request
        result = processor.process_demo_request(
            github_url=test_data["github_url"],
            requirements_path=test_data["requirements_path"],
            audience=test_data["audience"],
            purpose=test_data["purpose"],
            demo_duration=test_data["demo_duration"]
        )
        
        print("✅ Unified processor test passed")
        print(f"   - Generated script: {len(result.get('presentation_script', ''))} chars")
        print(f"   - Demo steps: {len(result.get('demo_plan', {}).get('steps', []))}")
        print(f"   - Avatar segments: {len(result.get('avatar_script', {}).get('presentation', {}).get('segments', []))}")
        
    except Exception as e:
        print(f"❌ Unified processor test failed: {e}")
        return False
    
    # Step 2: Test Simple Avatar Presenter
    print("\n2️⃣ Testing Simple Avatar Presenter...")
    try:
        avatar_presenter = SimpleAvatarPresenter()
        
        # Load script
        avatar_presenter.load_script(
            result.get('presentation_script', ''),
            result.get('demo_plan', {})
        )
        
        print("✅ Avatar presenter test passed")
        print(f"   - Loaded {len(avatar_presenter.segments)} segments")
        print(f"   - Total duration: {sum(seg.duration for seg in avatar_presenter.segments):.1f} seconds")
        
        # Test avatar script generation
        avatar_script = avatar_presenter.generate_avatar_script()
        print(f"   - Generated avatar script with {len(avatar_script['presentation']['segments'])} segments")
        
        # Test embed code generation
        embed_code = avatar_presenter.generate_embed_code("test_presentation")
        print(f"   - Generated embed code: {len(embed_code)} chars")
        
        # Test presentation summary
        summary = avatar_presenter.get_presentation_summary()
        print(f"   - Summary: {summary['segment_count']} segments, {summary['total_duration']:.1f}s duration")
        
    except Exception as e:
        print(f"❌ Avatar presenter test failed: {e}")
        return False
    
    # Step 3: Test Avatar Script Structure
    print("\n3️⃣ Testing Avatar Script Structure...")
    try:
        avatar_script = result.get('avatar_script', {})
        
        # Check required fields
        required_fields = ['avatar_config', 'presentation', 'timing']
        for field in required_fields:
            if field not in avatar_script:
                print(f"   ❌ Missing required field: {field}")
                return False
        
        # Check presentation segments
        segments = avatar_script['presentation'].get('segments', [])
        if not segments:
            print("   ❌ No presentation segments found")
            return False
        
        # Check segment structure
        for i, segment in enumerate(segments):
            required_segment_fields = ['id', 'text', 'duration', 'gesture']
            for field in required_segment_fields:
                if field not in segment:
                    print(f"   ❌ Segment {i+1} missing field: {field}")
                    return False
        
        print("✅ Avatar script structure test passed")
        print(f"   - {len(segments)} segments with proper structure")
        print(f"   - Timing: {avatar_script['timing'].get('total_duration', 0):.1f}s")
        print(f"   - Pauses: {avatar_script['timing'].get('pause_count', 0)}")
        
    except Exception as e:
        print(f"❌ Avatar script structure test failed: {e}")
        return False
    
    # Step 4: Test Sample Presentation
    print("\n4️⃣ Testing Sample Presentation...")
    try:
        # Create sample script
        sample_script = """
        Welcome to our demo! Today I'm going to show you how our platform revolutionizes team collaboration.
        
        Let me start by explaining the core problem we're solving. Traditional collaboration tools are fragmented and don't provide the seamless experience that modern teams need.
        
        Now, let me show you our solution. As you can see, we've created an intuitive interface that brings everything together in one place.
        
        Here's how it works. Users can create projects, assign tasks, and track progress all from a single dashboard. The system automatically syncs across all devices.
        
        Let me demonstrate the key features. First, you'll notice the clean, modern design. Everything is organized logically and easy to find.
        
        The real magic happens when you start collaborating. Team members can see updates in real-time, comment on tasks, and receive notifications instantly.
        
        In conclusion, our platform provides everything teams need to work efficiently and stay connected. Thank you for your attention!
        """
        
        # Test with sample script
        sample_presenter = SimpleAvatarPresenter()
        sample_presenter.load_script(sample_script)
        
        sample_script_result = sample_presenter.generate_avatar_script()
        sample_summary = sample_presenter.get_presentation_summary()
        
        print("✅ Sample presentation test passed")
        print(f"   - Segments: {sample_summary['segment_count']}")
        print(f"   - Duration: {sample_summary['total_duration']:.1f}s")
        print(f"   - Pauses: {sample_summary['pause_count']}")
        
        # Show sample segments
        print("   📋 Sample segments:")
        for i, segment in enumerate(sample_summary['segments'][:3], 1):
            print(f"      {i}. {segment['text_preview']}")
            print(f"         Duration: {segment['duration']:.1f}s | Gesture: {segment['gesture']}")
        
    except Exception as e:
        print(f"❌ Sample presentation test failed: {e}")
        return False
    
    # Step 5: Save Test Results
    print("\n5️⃣ Saving Test Results...")
    try:
        test_output_dir = Path("test_outputs")
        test_output_dir.mkdir(exist_ok=True)
        
        # Save complete results
        test_results = {
            "test_data": test_data,
            "processor_result": result,
            "avatar_script": avatar_script,
            "sample_presentation": {
                "segments": sample_summary['segments'],
                "total_duration": sample_summary['total_duration'],
                "pause_count": sample_summary['pause_count']
            },
            "status": "PASSED"
        }
        
        with open(test_output_dir / "simple_avatar_test.json", "w") as f:
            json.dump(test_results, f, indent=2)
        
        # Save embed code for manual testing
        embed_code = avatar_presenter.generate_embed_code("test_presentation")
        with open(test_output_dir / "avatar_embed_code.html", "w") as f:
            f.write(embed_code)
        
        print("✅ Test results saved to test_outputs/")
        print("   - simple_avatar_test.json: Complete test results")
        print("   - avatar_embed_code.html: Embed code for manual testing")
        
    except Exception as e:
        print(f"❌ Failed to save test results: {e}")
        return False
    
    print("\n🎉 All Simple Avatar Tests Passed!")
    print("=" * 50)
    print("✅ Unified Processor: Working")
    print("✅ Simple Avatar Presenter: Working")
    print("✅ Avatar Script Structure: Valid")
    print("✅ Sample Presentation: Working")
    print("✅ Test Results: Saved")
    
    print("\n🚀 Ready to use!")
    print("Next steps:")
    print("1. Set your Llama API key")
    print("2. Set your Tavus API key (optional)")
    print("3. Run: streamlit run src/ui/demo_ui.py")
    print("4. Upload requirements and generate your demo!")
    
    return True

def test_avatar_without_llama():
    """Test avatar functionality without Llama API"""
    
    print("\n🧪 Testing Avatar Without Llama API...")
    print("=" * 40)
    
    try:
        # Create avatar presenter
        avatar_presenter = SimpleAvatarPresenter()
        
        # Test with sample script
        sample_script = """
        Hello! Welcome to our demo. Today I'm going to show you something amazing.
        
        Let me start by explaining what we've built. This is a revolutionary platform that changes everything.
        
        Now, let me demonstrate the key features. As you can see, the interface is clean and intuitive.
        
        Here's how it works. Users simply click here, and everything happens automatically.
        
        The results are incredible. Performance is 10x faster than traditional solutions.
        
        In conclusion, this platform will transform how you work. Thank you for your time!
        """
        
        # Load script
        avatar_presenter.load_script(sample_script)
        
        # Generate avatar script
        avatar_script = avatar_presenter.generate_avatar_script()
        
        # Generate embed code
        embed_code = avatar_presenter.generate_embed_code("sample_presentation")
        
        # Get summary
        summary = avatar_presenter.get_presentation_summary()
        
        print("✅ Avatar test without Llama passed")
        print(f"   - Segments: {summary['segment_count']}")
        print(f"   - Duration: {summary['total_duration']:.1f}s")
        print(f"   - Pauses: {summary['pause_count']}")
        
        # Save sample embed code
        test_output_dir = Path("test_outputs")
        test_output_dir.mkdir(exist_ok=True)
        
        with open(test_output_dir / "sample_avatar_embed.html", "w") as f:
            f.write(embed_code)
        
        print("   💾 Sample embed code saved to test_outputs/sample_avatar_embed.html")
        
        return True
        
    except Exception as e:
        print(f"❌ Avatar test without Llama failed: {e}")
        return False

def main():
    """Run all tests"""
    
    print("🎭 DemoAM Simple Avatar Test Suite")
    print("=" * 50)
    
    # Test without Llama first
    avatar_only_success = test_avatar_without_llama()
    
    if avatar_only_success:
        print("\n✅ Avatar functionality works independently!")
        
        # Ask if user wants to test with Llama
        print("\n🤔 Do you want to test with Llama API? (requires LLAMA_API_KEY)")
        print("   This will test the complete integration including script generation.")
        
        # For now, just show that avatar works
        print("\n🎉 Avatar integration is ready!")
        print("You can now:")
        print("1. Run the UI: streamlit run src/ui/demo_ui.py")
        print("2. Test with sample scripts")
        print("3. Add your Llama API key for full functionality")
        
    else:
        print("\n❌ Avatar functionality has issues")
        print("Please check the error messages above")

if __name__ == "__main__":
    main() 