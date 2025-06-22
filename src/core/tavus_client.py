#!/usr/bin/env python3
"""
Tavus Client - Real integration with Tavus API for avatar creation and control
"""

import os
import json
import requests
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class TavusConfig:
    """Configuration for Tavus API"""
    api_key: str
    base_url: str = "https://tavusapi.com"  # Correct Tavus API endpoint from docs
    timeout: int = 30

@dataclass
class VideoRequest:
    """Request for video generation"""
    script: str
    replica_id: str = "default"  # You can specify a specific replica ID
    background_url: Optional[str] = None
    custom_instructions: Optional[str] = None

@dataclass
class VideoResponse:
    """Response from video generation"""
    video_id: str
    status: str
    embed_url: Optional[str] = None
    preview_url: Optional[str] = None
    duration: Optional[float] = None

class TavusClient:
    """Real Tavus API client for video generation and management"""
    
    def __init__(self, config: Optional[TavusConfig] = None):
        self.config = config or TavusConfig(
            api_key=os.getenv("TAVUS_API_KEY")
        )
        
        if not self.config.api_key:
            raise ValueError("TAVUS_API_KEY environment variable is required")
        
        self.headers = {
            "x-api-key": self.config.api_key,  # Correct header format from docs
            "Content-Type": "application/json"
        }
    
    def create_video(self, request: VideoRequest) -> VideoResponse:
        """Create a new video with the given script"""
        
        # Safety check: Prevent videos longer than 1 minute to conserve credits
        script_length = len(request.script)
        estimated_duration = script_length / 150  # Rough estimate: 150 words per minute
        
        if estimated_duration > 1.0:
            print(f"⚠️ WARNING: Script is {estimated_duration:.1f} minutes long. Truncating to ~1 minute to conserve Tavus credits.")
            # Truncate script to approximately 1 minute
            max_words = 150  # 1 minute at 150 words per minute
            words = request.script.split()[:max_words]
            request.script = " ".join(words) + "..."
            print(f"📝 Truncated script to {len(words)} words (~1 minute)")
        
        print("🎭 Creating Tavus video...")
        print(f"🔗 API URL: {self.config.base_url}/v2/videos")
        
        # Hardcode a valid replica_id
        hardcoded_replica_id = "re1074c227"  # Replace with your preferred valid replica_id
        
        # Prepare the request payload based on Tavus API docs
        payload = {
            "replica_id": hardcoded_replica_id,
            "script": request.script,
            "video_name": "Demo Presentation",
            "background_url": request.background_url or ""
        }
        
        try:
            print(f"📤 Sending request to Tavus API...")
            print(f"📋 Payload: {json.dumps(payload, indent=2)}")
            
            # Make API call to create video using correct endpoint from docs
            response = requests.post(
                f"{self.config.base_url}/v2/videos",
                headers=self.headers,
                json=payload,
                timeout=self.config.timeout
            )
            
            print(f"📥 Response status: {response.status_code}")
            print(f"📥 Response headers: {dict(response.headers)}")
            
            if response.status_code != 200:
                print(f"📥 Response body: {response.text}")
            
            response.raise_for_status()
            data = response.json()
            
            print(f"✅ Video created: {data.get('video_id', 'Unknown')}")
            
            return VideoResponse(
                video_id=data.get('video_id'),
                status=data.get('status', 'queued'),
                embed_url=data.get('hosted_url'),  # Use hosted_url for embedding
                preview_url=data.get('hosted_url'),
                duration=None  # Duration not provided in initial response
            )
            
        except requests.exceptions.ConnectionError as e:
            print(f"❌ Connection error: {str(e)}")
            print(f"💡 Please check your internet connection and verify the Tavus API endpoint")
            raise Exception(f"Failed to connect to Tavus API: {str(e)}")
            
        except requests.exceptions.Timeout as e:
            print(f"❌ Timeout error: {str(e)}")
            raise Exception(f"Tavus API request timed out: {str(e)}")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Tavus API error: {str(e)}")
            print(f"💡 Please verify your TAVUS_API_KEY and check Tavus documentation")
            raise Exception(f"Failed to create Tavus video: {str(e)}")
    
    def get_video_status(self, video_id: str) -> Dict[str, Any]:
        """Get the status of a video using correct endpoint from docs"""
        
        try:
            response = requests.get(
                f"{self.config.base_url}/v2/videos/{video_id}",
                headers={"x-api-key": self.config.api_key},  # Only x-api-key header for GET
                timeout=self.config.timeout
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error getting video status: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def wait_for_completion(self, video_id: str, max_wait: int = 300) -> bool:
        """Wait for video to complete processing"""
        
        print(f"⏳ Waiting for video to complete...")
        
        start_time = time.time()
        while time.time() - start_time < max_wait:
            status_data = self.get_video_status(video_id)
            status = status_data.get('status', 'unknown')
            
            if status == 'ready':
                print("✅ Video ready!")
                return True
            elif status == 'error':
                print("❌ Video failed!")
                return False
            elif status in ['queued', 'generating']:
                print(f"⏳ Still processing... ({status})")
                time.sleep(10)  # Wait 10 seconds before checking again
            else:
                print(f"⚠️ Unknown status: {status}")
                time.sleep(10)
        
        print("⏰ Timeout waiting for video completion")
        return False
    
    def generate_embed_code(self, video_id: str, hosted_url: str = None, width: int = 800, height: int = 600) -> str:
        """Generate HTML embed code for the video"""
        
        # Use hosted_url if provided, otherwise construct default embed URL
        if hosted_url:
            embed_url = hosted_url
        else:
            embed_url = f"https://app.tavus.com/embed/{video_id}"
        
        return f"""
        <div id="tavus-player-container" style="width: 100%; max-width: {width}px; margin: 0 auto;">
            <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
                <h3 style="margin: 0 0 10px 0; color: #667eea;">🎭 Tavus Avatar Video</h3>
                <p style="margin: 0; color: #666;">Loading your personalized avatar video...</p>
            </div>
            
            <iframe 
                src="{embed_url}"
                width="100%" 
                height="{height}px" 
                frameborder="0"
                allowfullscreen
                style="border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            </iframe>
            
            <div style="margin-top: 20px; text-align: center; color: #666; font-size: 14px;">
                <p>🎬 Your avatar will read the generated script with natural pauses and gestures</p>
                <p>⏱️ Duration: Based on your specified demo length</p>
                <p>🎯 Audience: Tailored for your selected audience</p>
            </div>
        </div>
        """
    
    def _get_default_instructions(self) -> str:
        """Get default custom instructions for the avatar"""
        
        return """
        Please present this script in a professional, engaging manner:
        - Use natural pauses between sections
        - Emphasize key points and technical details
        - Maintain a conversational tone
        - Use appropriate gestures to enhance the presentation
        - Adapt the pace to match the technical complexity
        - Ensure clear pronunciation of technical terms
        """
    
    def create_presentation_from_script(self, script: str, audience: str = "Mixed", purpose: str = "Demo") -> Dict[str, Any]:
        """Create a complete presentation from the generated script"""
        
        # Customize instructions based on audience and purpose
        custom_instructions = f"""
        Present this {purpose} for a {audience} audience:
        - Use appropriate technical depth for {audience}
        - Focus on {purpose} aspects
        - Maintain professional but engaging delivery
        - Use natural pauses and gestures
        - Emphasize key features and benefits
        """
        
        # Create video request
        request = VideoRequest(
            script=script,
            replica_id="default",  # You can change this to specific replica ID
            custom_instructions=custom_instructions
        )
        
        # Create the video
        response = self.create_video(request)
        
        # Wait for completion
        if self.wait_for_completion(response.video_id):
            # Get final status
            final_status = self.get_video_status(response.video_id)
            
            # Get the hosted URL from the final status
            hosted_url = final_status.get('hosted_url')
            
            return {
                "presentation_id": response.video_id,
                "status": "completed",
                "embed_url": hosted_url,
                "preview_url": hosted_url,
                "duration": None,  # Duration not provided by Tavus API
                "embed_code": self.generate_embed_code(response.video_id, hosted_url),
                "final_status": final_status
            }
        else:
            return {
                "presentation_id": response.video_id,
                "status": "failed",
                "error": "Video processing failed or timed out"
            } 