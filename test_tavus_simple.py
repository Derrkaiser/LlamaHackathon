#!/usr/bin/env python3
"""
Simple Tavus API Test - Test with correct endpoints from docs
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def test_tavus_api():
    """Test Tavus API with correct endpoints from documentation"""
    
    api_key = os.getenv("TAVUS_API_KEY")
    if not api_key:
        print("❌ TAVUS_API_KEY not found in environment")
        return False
    
    print(f"🔑 API Key found: {api_key[:10]}...")
    
    # Test video creation with correct format from docs
    url = "https://tavusapi.com/v2/videos"
    
    payload = {
        "background_url": "",
        "replica_id": "default",  # Use default replica
        "script": "Hello, this is a test video for our demo presentation. We're testing the Tavus API integration.",
        "video_name": "Demo Test Video"
    }
    
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    print(f"\n🎭 Testing Tavus Video Creation")
    print(f"🔗 URL: {url}")
    print(f"📋 Payload: {json.dumps(payload, indent=2)}")
    print(f"📋 Headers: {list(headers.keys())}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"📥 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS! Video created")
            print(f"📄 Response: {json.dumps(data, indent=2)}")
            
            video_id = data.get('video_id')
            if video_id:
                print(f"🎬 Video ID: {video_id}")
                
                # Test getting video status
                print(f"\n🔍 Testing video status...")
                status_url = f"https://tavusapi.com/v2/videos/{video_id}"
                status_headers = {"x-api-key": api_key}
                
                status_response = requests.get(status_url, headers=status_headers, timeout=10)
                print(f"📥 Status Response: {status_response.status_code}")
                
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f"📄 Status Data: {json.dumps(status_data, indent=2)}")
                    return True
                else:
                    print(f"❌ Status check failed: {status_response.text}")
                    return False
            else:
                print("❌ No video_id in response")
                return False
                
        elif response.status_code == 400:
            print(f"📝 Bad Request: {response.text}")
            print("💡 This might be due to missing required fields or invalid replica_id")
            return False
        elif response.status_code == 401:
            print(f"🔒 Unauthorized: {response.text}")
            print("💡 Check your API key")
            return False
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {str(e)}")
        return False
    except requests.exceptions.Timeout as e:
        print(f"⏰ Timeout: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Tavus API Simple Test")
    print("=" * 40)
    
    success = test_tavus_api()
    
    if success:
        print(f"\n🎉 Tavus API test PASSED!")
        print(f"✅ Video creation works")
        print(f"✅ Status checking works")
    else:
        print(f"\n❌ Tavus API test FAILED!")
        print(f"💡 Please check:")
        print(f"   1. Your TAVUS_API_KEY is correct")
        print(f"   2. You have proper API access")
        print(f"   3. Your account is active")
        print(f"   4. You have available video credits") 