#!/usr/bin/env python3
"""
Test Tavus Replicas - Get available replicas from Tavus API
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def get_tavus_replicas():
    """Get available replicas from Tavus API"""
    
    api_key = os.getenv("TAVUS_API_KEY")
    if not api_key:
        print("❌ TAVUS_API_KEY not found in environment")
        return None
    
    print(f"🔑 API Key found: {api_key[:10]}...")
    
    # Try to get replicas
    url = "https://tavusapi.com/v2/replicas"
    
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    print(f"\n🎭 Getting Tavus Replicas")
    print(f"🔗 URL: {url}")
    print(f"📋 Headers: {list(headers.keys())}")
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        print(f"📥 Response Status: {response.status_code}")
        print(f"📥 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS! Got replicas")
            
            # Handle the actual response structure
            if 'data' in data and isinstance(data['data'], list):
                replicas = data['data']
                print(f"📄 Found {len(replicas)} replicas")
                return replicas
            elif isinstance(data, list):
                print(f"📄 Found {len(data)} replicas")
                return data
            else:
                print(f"📄 Unexpected response structure: {json.dumps(data, indent=2)}")
                return None
        elif response.status_code == 401:
            print(f"🔒 Unauthorized: {response.text}")
            print("💡 Check your API key")
            return None
        elif response.status_code == 404:
            print(f"🔍 Endpoint not found: {response.text}")
            print("💡 This endpoint might not exist")
            return None
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection error: {str(e)}")
        return None
    except requests.exceptions.Timeout as e:
        print(f"⏰ Timeout: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_with_replica_id(replica_id):
    """Test video creation with a specific replica ID"""
    
    api_key = os.getenv("TAVUS_API_KEY")
    if not api_key:
        print("❌ TAVUS_API_KEY not found in environment")
        return False
    
    url = "https://tavusapi.com/v2/videos"
    
    payload = {
        "background_url": "",
        "replica_id": replica_id,
        "script": "Hello, this is a test video for our demo presentation. We're testing the Tavus API integration.",
        "video_name": "Demo Test Video"
    }
    
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    print(f"\n🎭 Testing with replica_id: {replica_id}")
    print(f"🔗 URL: {url}")
    print(f"📋 Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS! Video created with replica {replica_id}")
            print(f"📄 Response: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Tavus Replicas Test")
    print("=" * 40)
    
    # First, try to get replicas
    replicas = get_tavus_replicas()
    
    if replicas and len(replicas) > 0:
        print(f"\n🎉 Found {len(replicas)} replicas!")
        
        # Show first few replicas
        print(f"\n📋 First 5 replicas:")
        for i, replica in enumerate(replicas[:5]):
            replica_id = replica.get('replica_id', 'Unknown')
            replica_name = replica.get('replica_name', 'Unknown')
            status = replica.get('status', 'Unknown')
            print(f"   {i+1}. {replica_name} (ID: {replica_id}) - Status: {status}")
        
        # Try the first replica
        first_replica = replicas[0]
        replica_id = first_replica.get('replica_id')
        
        if replica_id:
            print(f"\n🎭 Testing with first replica: {replica_id}")
            success = test_with_replica_id(replica_id)
            
            if success:
                print(f"\n🎉 SUCCESS! Use replica_id: {replica_id}")
                print(f"💡 You can now use this replica_id in your Tavus client")
            else:
                print(f"\n❌ Failed with replica_id: {replica_id}")
                
                # Try a few more replicas
                print(f"\n🧪 Trying a few more replicas...")
                for i, replica in enumerate(replicas[1:4]):
                    replica_id = replica.get('replica_id')
                    if replica_id:
                        print(f"\n🎭 Testing replica {i+2}: {replica_id}")
                        success = test_with_replica_id(replica_id)
                        if success:
                            print(f"🎉 SUCCESS! Use replica_id: {replica_id}")
                            break
        else:
            print(f"❌ No valid replica_id found in first replica")
    else:
        print(f"\n❌ Could not get replicas")
        print(f"💡 You may need to:")
        print(f"   1. Create a replica in your Tavus dashboard")
        print(f"   2. Check your API permissions")
        print(f"   3. Use a different API endpoint")
        
        # Try with a common default replica ID
        print(f"\n🧪 Trying with common default replica IDs...")
        common_replicas = ["default", "demo", "test", "presenter"]
        
        for replica_id in common_replicas:
            print(f"\n🎭 Testing replica_id: {replica_id}")
            success = test_with_replica_id(replica_id)
            if success:
                print(f"🎉 SUCCESS! Use replica_id: {replica_id}")
                break 