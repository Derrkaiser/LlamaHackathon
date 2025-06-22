#!/usr/bin/env python3
"""
Get Tavus Video URL - Simple script to retrieve the embed URL for a generated video
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_video_url(video_id: str):
    """Get the embed URL for a Tavus video"""
    
    api_key = os.getenv("TAVUS_API_KEY")
    if not api_key:
        print("❌ TAVUS_API_KEY not found in environment")
        return
    
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        # Get video status
        response = requests.get(
            f"https://tavusapi.com/v2/videos/{video_id}",
            headers=headers,
            timeout=30
        )
        
        response.raise_for_status()
        data = response.json()
        
        print(f"🎬 Video Status: {data.get('status', 'unknown')}")
        print(f"📋 Video Data: {data}")
        
        # Try different possible URL fields
        hosted_url = data.get('hosted_url')
        embed_url = data.get('embed_url')
        preview_url = data.get('preview_url')
        
        print("\n🔗 Possible URLs:")
        if hosted_url:
            print(f"   Hosted URL: {hosted_url}")
        if embed_url:
            print(f"   Embed URL: {embed_url}")
        if preview_url:
            print(f"   Preview URL: {preview_url}")
        
        # Construct default URLs
        print(f"\n🔗 Default URLs:")
        print(f"   Tavus App: https://app.tavus.com/video/{video_id}")
        print(f"   Embed URL: https://app.tavus.com/embed/{video_id}")
        
        return hosted_url or embed_url or preview_url
        
    except Exception as e:
        print(f"❌ Error getting video URL: {str(e)}")
        return None

if __name__ == "__main__":
    # Your video ID from the logs
    video_id = "f6898a5b37"
    
    print(f"🎭 Getting URL for video: {video_id}")
    print("=" * 50)
    
    url = get_video_url(video_id)
    
    if url:
        print(f"\n✅ Direct URL: {url}")
    else:
        print(f"\n💡 Try these URLs manually:")
        print(f"   https://app.tavus.com/video/{video_id}")
        print(f"   https://app.tavus.com/embed/{video_id}") 