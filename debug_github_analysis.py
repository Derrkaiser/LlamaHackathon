"""
Debug GitHub Analysis - Test the GitHub ingestion step by step
"""

import asyncio
import os
import json
from src.core.unified_processor import UnifiedProcessor

async def debug_github_analysis():
    """Debug the GitHub analysis process step by step"""
    
    api_key = os.getenv("LLAMA_API_KEY")
    if not api_key:
        print("❌ LLAMA_API_KEY not found")
        return
    
    print("🔍 Debugging GitHub Analysis")
    print("=" * 40)
    
    github_url = "https://github.com/cyclotruc/gitingest"
    
    # Step 1: Test gitingest directly
    print("\n1️⃣ Testing gitingest library...")
    try:
        from gitingest import ingest_async
        summary, tree, content = await ingest_async(github_url)
        
        print(f"✅ gitingest successful!")
        print(f"   Summary length: {len(summary)} chars")
        print(f"   Tree length: {len(tree)} chars")
        print(f"   Content length: {len(content)} chars")
        
        print(f"\n📋 Summary preview:")
        print(summary[:500] + "..." if len(summary) > 500 else summary)
        
        print(f"\n🌳 Tree structure preview:")
        print(tree[:500] + "..." if len(tree) > 500 else tree)
        
        print(f"\n📄 Content preview:")
        print(content[:500] + "..." if len(content) > 500 else content)
        
    except Exception as e:
        print(f"❌ gitingest failed: {e}")
        return
    
    # Step 2: Test Llama analysis
    print("\n2️⃣ Testing Llama analysis...")
    try:
        processor = UnifiedProcessor(api_key)
        
        # Build the analysis prompt
        analysis_prompt = f"""
        Analyze this codebase and extract key insights in JSON format:
        
        REPOSITORY SUMMARY:
        {summary}
        
        FILE STRUCTURE:
        {tree}
        
        CODE CONTENT:
        {content[:3000]}  # Limit content for API call
        
        Provide structured analysis in this exact JSON format:
        {{
            "architecture": "main tech stack and architectural patterns",
            "main_features": ["list of 3-5 key features"],
            "dependencies": ["main dependencies and frameworks"],
            "key_components": ["core modules/components"],
            "user_flows": ["main user journeys and workflows"]
        }}
        
        Focus on understanding the application's purpose, architecture, and key functionality.
        """
        
        print(f"📤 Sending prompt to Llama...")
        response = await processor.llama_client._call_llama(analysis_prompt)
        
        print(f"📥 Llama response received!")
        print(f"   Response length: {len(response)} chars")
        print(f"   Response preview: {response[:200]}...")
        
        # Try to parse JSON
        try:
            analysis_data = json.loads(response)
            print(f"✅ JSON parsing successful!")
            print(f"   Architecture: {analysis_data.get('architecture', 'N/A')}")
            print(f"   Features: {analysis_data.get('main_features', [])}")
            print(f"   Dependencies: {analysis_data.get('dependencies', [])}")
            print(f"   Components: {analysis_data.get('key_components', [])}")
            print(f"   User Flows: {analysis_data.get('user_flows', [])}")
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print(f"   Raw response: {response}")
            
    except Exception as e:
        print(f"❌ Llama analysis failed: {e}")
    
    # Step 3: Test the full process
    print("\n3️⃣ Testing full GitHub analysis process...")
    try:
        result = await processor._process_github_codebase(github_url)
        print(f"✅ Full process successful!")
        print(f"   Architecture: {result.architecture}")
        print(f"   Features: {result.main_features}")
        print(f"   Dependencies: {result.dependencies}")
        print(f"   Components: {result.key_components}")
        print(f"   User Flows: {result.user_flows}")
        
    except Exception as e:
        print(f"❌ Full process failed: {e}")
    
    await processor.llama_client.close()

if __name__ == "__main__":
    asyncio.run(debug_github_analysis()) 