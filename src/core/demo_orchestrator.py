#!/usr/bin/env python3
"""
Demo Orchestrator - Coordinates Tavus avatar presentation with browser automation
"""

import asyncio
import json
import time
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import threading
from datetime import datetime

@dataclass
class DemoEvent:
    """Represents a demo event with timing and actions"""
    event_id: str
    timestamp: float
    avatar_action: str
    browser_action: Optional[str] = None
    completion_signal: Optional[str] = None
    duration: float = 5.0

class DemoOrchestrator:
    """Orchestrates synchronized demo with avatar and browser automation"""
    
    def __init__(self):
        self.events: List[DemoEvent] = []
        self.current_event_index = 0
        self.is_running = False
        self.avatar_ready = False
        self.browser_ready = False
        self.completion_signals = {}
        self.event_callbacks = {}
        
    def load_demo_script(self, avatar_script: Dict[str, Any], browser_actions: List[str]):
        """Load demo script with avatar and browser coordination"""
        
        self.events = []
        current_time = 0.0
        
        # Extract avatar segments
        avatar_segments = avatar_script.get('avatar_script', {}).get('presentation', {}).get('segments', [])
        demo_coordination = avatar_script.get('avatar_script', {}).get('demo_coordination', {})
        
        for i, segment in enumerate(avatar_segments):
            segment_id = segment.get('id', f'segment_{i+1}')
            duration = segment.get('duration', 10.0)
            
            # Check if this segment has demo coordination
            browser_action = None
            completion_signal = None
            
            if segment_id in demo_coordination:
                demo_info = demo_coordination[segment_id]
                action_id = demo_info.get('action_id', f'action_{i+1}')
                
                # Find corresponding browser action
                if i < len(browser_actions):
                    browser_action = browser_actions[i]
                    completion_signal = demo_info.get('completion_signal', f'signal_{i+1}')
            
            event = DemoEvent(
                event_id=segment_id,
                timestamp=current_time,
                avatar_action=segment.get('text', ''),
                browser_action=browser_action,
                completion_signal=completion_signal,
                duration=duration
            )
            
            self.events.append(event)
            current_time += duration
    
    async def start_demo(self, demo_url: str):
        """Start the synchronized demo"""
        
        if not self.events:
            raise ValueError("No demo events loaded. Call load_demo_script() first.")
        
        self.is_running = True
        self.current_event_index = 0
        
        print(f"🚀 Starting synchronized demo with {len(self.events)} events")
        print(f"🌐 Demo URL: {demo_url}")
        
        # Start browser automation in background
        browser_thread = threading.Thread(
            target=self._run_browser_automation,
            args=(demo_url,)
        )
        browser_thread.start()
        
        # Start avatar presentation
        await self._run_avatar_presentation()
        
        # Wait for completion
        browser_thread.join()
        
        print("✅ Demo completed successfully!")
    
    async def _run_avatar_presentation(self):
        """Run avatar presentation with timing coordination"""
        
        for i, event in enumerate(self.events):
            if not self.is_running:
                break
                
            self.current_event_index = i
            
            print(f"🎭 Avatar Event {i+1}/{len(self.events)}: {event.avatar_action[:50]}...")
            
            # Signal avatar to start this segment
            await self._signal_avatar_start(event)
            
            # Wait for segment duration
            await asyncio.sleep(event.duration)
            
            # Signal completion if there was a browser action
            if event.completion_signal:
                self.completion_signals[event.completion_signal] = True
                print(f"✅ Completed: {event.completion_signal}")
    
    def _run_browser_automation(self, demo_url: str):
        """Run browser automation in background thread"""
        
        try:
            print(f"🌐 Starting browser automation for: {demo_url}")
            
            # Import browser automation here to avoid blocking
            from .browser_agent import BrowserAgent
            
            agent = BrowserAgent(demo_url)
            
            for i, event in enumerate(self.events):
                if not self.is_running:
                    break
                
                # Wait for avatar to reach this event
                while self.current_event_index < i:
                    time.sleep(0.1)
                
                if event.browser_action:
                    print(f"🤖 Browser Action {i+1}: {event.browser_action}")
                    
                    # Execute browser action
                    success = agent.execute_action(event.browser_action)
                    
                    if success and event.completion_signal:
                        self.completion_signals[event.completion_signal] = True
                        print(f"✅ Browser action completed: {event.completion_signal}")
                    else:
                        print(f"⚠️ Browser action failed: {event.browser_action}")
                
                # Wait for event duration
                time.sleep(event.duration)
            
            agent.cleanup()
            
        except Exception as e:
            print(f"❌ Browser automation failed: {e}")
    
    async def _signal_avatar_start(self, event: DemoEvent):
        """Signal avatar to start a segment"""
        
        # This would integrate with Tavus API to control avatar
        print(f"🎭 Avatar starting: {event.avatar_action[:50]}...")
        
        # Simulate avatar API call
        avatar_data = {
            "segment_id": event.event_id,
            "text": event.avatar_action,
            "duration": event.duration,
            "gesture": self._get_gesture_for_action(event.browser_action) if event.browser_action else "presentation_gesture"
        }
        
        # Call avatar API (placeholder)
        await self._call_tavus_api(avatar_data)
    
    def _get_gesture_for_action(self, action: str) -> str:
        """Get appropriate gesture for browser action"""
        
        if not action:
            return "presentation_gesture"
        
        action_lower = action.lower()
        
        if any(word in action_lower for word in ['click', 'button', 'press']):
            return "point_at_screen"
        elif any(word in action_lower for word in ['type', 'enter', 'input']):
            return "typing_gesture"
        elif any(word in action_lower for word in ['scroll', 'navigate']):
            return "scroll_gesture"
        elif any(word in action_lower for word in ['wait', 'pause']):
            return "waiting_gesture"
        else:
            return "neutral_gesture"
    
    async def _call_tavus_api(self, avatar_data: Dict[str, Any]):
        """Call Tavus API to control avatar (placeholder)"""
        
        # This would be the actual Tavus API integration
        # For now, we'll simulate the API call
        
        try:
            # Simulate API call
            await asyncio.sleep(0.1)  # Simulate network delay
            
            print(f"🎭 Tavus API called: {avatar_data['segment_id']}")
            
        except Exception as e:
            print(f"❌ Tavus API error: {e}")
    
    def stop_demo(self):
        """Stop the demo"""
        self.is_running = False
        print("🛑 Demo stopped")
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current demo status"""
        
        if not self.events:
            return {"status": "no_events"}
        
        current_event = self.events[self.current_event_index] if self.current_event_index < len(self.events) else None
        
        return {
            "status": "running" if self.is_running else "stopped",
            "current_event": self.current_event_index + 1,
            "total_events": len(self.events),
            "current_event_data": {
                "id": current_event.event_id if current_event else None,
                "avatar_action": current_event.avatar_action if current_event else None,
                "browser_action": current_event.browser_action if current_event else None,
                "duration": current_event.duration if current_event else None
            },
            "completion_signals": self.completion_signals
        }
    
    def generate_embed_code(self, presentation_id: str) -> str:
        """Generate HTML embed code for Tavus player"""
        
        return f"""
        <div id="tavus-player-container" style="width: 100%; height: 400px; border: 2px solid #667eea; border-radius: 10px; overflow: hidden;">
            <iframe 
                src="https://app.tavus.com/embed/{presentation_id}"
                width="100%" 
                height="100%" 
                frameborder="0"
                allowfullscreen>
            </iframe>
        </div>
        <script>
            // Demo coordination script
            const demoEvents = {json.dumps([{
                'id': event.event_id,
                'timestamp': event.timestamp,
                'duration': event.duration,
                'browser_action': event.browser_action,
                'completion_signal': event.completion_signal
            } for event in self.events])};
            
            let currentEventIndex = 0;
            
            function startDemo() {{
                console.log('Starting synchronized demo...');
                // Start browser automation
                window.postMessage({{type: 'START_BROWSER_AUTOMATION'}}, '*');
                
                // Monitor avatar progress
                setInterval(() => {{
                    if (currentEventIndex < demoEvents.length) {{
                        const event = demoEvents[currentEventIndex];
                        console.log(`Event ${{currentEventIndex + 1}}: ${{event.browser_action || 'Avatar only'}}`);
                        
                        if (event.browser_action) {{
                            // Signal browser agent
                            window.postMessage({{
                                type: 'EXECUTE_BROWSER_ACTION',
                                action: event.browser_action,
                                completion_signal: event.completion_signal
                            }}, '*');
                        }}
                        
                        currentEventIndex++;
                    }}
                }}, 1000);
            }}
            
            // Listen for browser completion signals
            window.addEventListener('message', (event) => {{
                if (event.data.type === 'BROWSER_ACTION_COMPLETED') {{
                    console.log(`Browser action completed: ${{event.data.signal}}`);
                    // Signal avatar to continue
                    window.postMessage({{
                        type: 'AVATAR_CONTINUE',
                        signal: event.data.signal
                    }}, '*');
                }}
            }});
        </script>
        """

# Example usage
if __name__ == "__main__":
    # Example demo script
    avatar_script = {
        "avatar_script": {
            "presentation": {
                "segments": [
                    {"id": "segment_1", "text": "Welcome to our demo!", "duration": 5.0},
                    {"id": "segment_2", "text": "Let me show you the interface", "duration": 10.0},
                    {"id": "segment_3", "text": "Now let's test the functionality", "duration": 15.0}
                ]
            },
            "demo_coordination": {
                "segment_2": {
                    "action_id": "demo_action_1",
                    "completion_signal": "action_1_complete"
                },
                "segment_3": {
                    "action_id": "demo_action_2", 
                    "completion_signal": "action_2_complete"
                }
            }
        }
    }
    
    browser_actions = [
        "Click on the login button",
        "Enter credentials and submit",
        "Navigate to the dashboard"
    ]
    
    # Test orchestrator
    orchestrator = DemoOrchestrator()
    orchestrator.load_demo_script(avatar_script, browser_actions)
    
    print("Demo orchestrator ready!")
    print(f"Loaded {len(orchestrator.events)} events")
    
    # Generate embed code
    embed_code = orchestrator.generate_embed_code("demo_presentation_123")
    print("\nEmbed code generated successfully!") 