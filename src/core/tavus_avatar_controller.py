#!/usr/bin/env python3
"""
Tavus Avatar Controller - Orchestrates avatar presentations with demo synchronization
"""

import os
import json
import asyncio
import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import time

@dataclass
class AvatarSegment:
    """Represents a segment of avatar presentation with timing and actions"""
    start_time: float
    duration: float
    text: str
    gesture: Optional[str] = None
    demo_action: Optional[str] = None
    pause_for_demo: bool = False
    demo_completion_signal: Optional[str] = None

@dataclass
class DemoAction:
    """Represents a demo action that needs to be synchronized"""
    action_id: str
    description: str
    expected_duration: float
    ui_selectors: List[str]
    expected_outcome: str
    completion_signal: str
    avatar_gesture: Optional[str] = None

class TavusAvatarController:
    """Controls Tavus avatar presentations with demo synchronization"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.tavus.com"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def synthesize_avatar_script(
        self, 
        presentation_script: Dict[str, Any], 
        execution_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesize presentation script and execution plan into coordinated avatar presentation
        
        Args:
            presentation_script: Llama-generated presentation script
            execution_plan: Llama-generated demo execution plan
            
        Returns:
            Coordinated avatar presentation with timing and gestures
        """
        
        # Extract presentation sections
        sections = presentation_script.get('presentation_script', {}).get('sections', [])
        
        # Extract demo actions
        demo_actions = self._extract_demo_actions(execution_plan)
        
        # Create coordinated timeline
        timeline = self._create_coordinated_timeline(sections, demo_actions)
        
        # Generate avatar script with timing and gestures
        avatar_script = self._generate_avatar_script(timeline)
        
        return {
            "avatar_script": avatar_script,
            "timeline": timeline,
            "demo_coordination": self._create_demo_coordination(demo_actions),
            "metadata": {
                "total_duration": self._calculate_total_duration(timeline),
                "demo_actions_count": len(demo_actions),
                "sections_count": len(sections),
                "generated_at": datetime.now().isoformat()
            }
        }
    
    def _extract_demo_actions(self, execution_plan: Dict[str, Any]) -> List[DemoAction]:
        """Extract demo actions from execution plan"""
        demo_actions = []
        
        # Extract from automation steps
        automation_steps = execution_plan.get('demo_plan', {}).get('automation_steps', [])
        
        for i, step in enumerate(automation_steps):
            action = DemoAction(
                action_id=f"demo_action_{i+1}",
                description=step,
                expected_duration=5.0,  # Default 5 seconds per action
                ui_selectors=[],  # Will be extracted from step description
                expected_outcome="Action completed successfully",
                avatar_gesture=self._suggest_gesture_for_action(step),
                completion_signal=f"action_{i+1}_complete"
            )
            demo_actions.append(action)
        
        return demo_actions
    
    def _suggest_gesture_for_action(self, action_description: str) -> str:
        """Suggest appropriate avatar gesture for demo action"""
        action_lower = action_description.lower()
        
        if any(word in action_lower for word in ['click', 'button', 'press']):
            return "point_at_screen"
        elif any(word in action_lower for word in ['type', 'enter', 'input']):
            return "typing_gesture"
        elif any(word in action_lower for word in ['scroll', 'navigate']):
            return "scroll_gesture"
        elif any(word in action_lower for word in ['wait', 'pause']):
            return "waiting_gesture"
        elif any(word in action_lower for word in ['result', 'show', 'display']):
            return "highlight_result"
        else:
            return "neutral_gesture"
    
    def _create_coordinated_timeline(
        self, 
        sections: List[Dict], 
        demo_actions: List[DemoAction]
    ) -> List[AvatarSegment]:
        """Create coordinated timeline of avatar segments and demo actions"""
        
        timeline = []
        current_time = 0.0
        
        for section in sections:
            section_duration = section.get('duration', 60)  # Default 60 seconds
            section_content = section.get('content', '')
            demo_steps = section.get('demo_steps', [])
            
            # Split section into segments based on demo actions
            if demo_steps:
                segments = self._split_section_with_demos(
                    section_content, 
                    demo_steps, 
                    demo_actions,
                    current_time,
                    section_duration
                )
                timeline.extend(segments)
            else:
                # No demo steps, just presentation
                segment = AvatarSegment(
                    start_time=current_time,
                    duration=section_duration,
                    text=section_content,
                    gesture="presentation_gesture"
                )
                timeline.append(segment)
            
            current_time += section_duration
        
        return timeline
    
    def _split_section_with_demos(
        self, 
        content: str, 
        demo_steps: List[str], 
        demo_actions: List[DemoAction],
        start_time: float,
        total_duration: float
    ) -> List[AvatarSegment]:
        """Split section content to accommodate demo actions"""
        
        segments = []
        current_time = start_time
        
        # Calculate time per demo step
        demo_time_per_step = 10.0  # 10 seconds per demo step
        presentation_time = total_duration - (len(demo_steps) * demo_time_per_step)
        
        # Split content into parts
        content_parts = self._split_content_for_demos(content, len(demo_steps))
        
        for i, (content_part, demo_step) in enumerate(zip(content_parts, demo_steps)):
            # Presentation segment
            if content_part.strip():
                presentation_duration = presentation_time / len(content_parts)
                segment = AvatarSegment(
                    start_time=current_time,
                    duration=presentation_duration,
                    text=content_part,
                    gesture="presentation_gesture"
                )
                segments.append(segment)
                current_time += presentation_duration
            
            # Demo action segment
            if i < len(demo_actions):
                demo_action = demo_actions[i]
                segment = AvatarSegment(
                    start_time=current_time,
                    duration=demo_time_per_step,
                    text=f"Now let me demonstrate: {demo_step}",
                    gesture=demo_action.avatar_gesture,
                    demo_action=demo_action.action_id,
                    pause_for_demo=True,
                    demo_completion_signal=demo_action.completion_signal
                )
                segments.append(segment)
                current_time += demo_time_per_step
        
        return segments
    
    def _split_content_for_demos(self, content: str, num_demos: int) -> List[str]:
        """Split content into parts to accommodate demo actions"""
        if num_demos == 0:
            return [content]
        
        # Simple split - can be enhanced with more sophisticated text analysis
        sentences = content.split('. ')
        sentences_per_part = max(1, len(sentences) // (num_demos + 1))
        
        parts = []
        for i in range(0, len(sentences), sentences_per_part):
            part = '. '.join(sentences[i:i + sentences_per_part])
            if part.strip():
                parts.append(part)
        
        # Ensure we have enough parts
        while len(parts) < num_demos + 1:
            parts.append("")
        
        return parts[:num_demos + 1]
    
    def _generate_avatar_script(self, timeline: List[AvatarSegment]) -> Dict[str, Any]:
        """Generate Tavus avatar script with timing and gestures"""
        
        avatar_script = {
            "presentation": {
                "title": "AI-Powered Demo Presentation",
                "segments": []
            },
            "gestures": {},
            "timing": {},
            "demo_coordination": {}
        }
        
        for i, segment in enumerate(timeline):
            segment_id = f"segment_{i+1}"
            
            # Add presentation segment
            avatar_script["presentation"]["segments"].append({
                "id": segment_id,
                "text": segment.text,
                "duration": segment.duration,
                "start_time": segment.start_time
            })
            
            # Add gesture if specified
            if segment.gesture:
                avatar_script["gestures"][segment_id] = {
                    "type": segment.gesture,
                    "start_time": segment.start_time,
                    "duration": segment.duration
                }
            
            # Add demo coordination if needed
            if segment.pause_for_demo:
                avatar_script["demo_coordination"][segment_id] = {
                    "action_id": segment.demo_action,
                    "completion_signal": segment.demo_completion_signal,
                    "pause_duration": segment.duration,
                    "gesture": segment.gesture
                }
        
        return avatar_script
    
    def _create_demo_coordination(self, demo_actions: List[DemoAction]) -> Dict[str, Any]:
        """Create demo coordination instructions"""
        
        coordination = {
            "demo_actions": [],
            "signals": {},
            "timing": {}
        }
        
        for action in demo_actions:
            coordination["demo_actions"].append({
                "id": action.action_id,
                "description": action.description,
                "expected_duration": action.expected_duration,
                "ui_selectors": action.ui_selectors,
                "expected_outcome": action.expected_outcome,
                "completion_signal": action.completion_signal
            })
            
            coordination["signals"][action.completion_signal] = {
                "action_id": action.action_id,
                "description": f"Signal when {action.description} is complete"
            }
        
        return coordination
    
    def _calculate_total_duration(self, timeline: List[AvatarSegment]) -> float:
        """Calculate total presentation duration"""
        if not timeline:
            return 0.0
        
        last_segment = timeline[-1]
        return last_segment.start_time + last_segment.duration
    
    async def create_avatar_presentation(self, avatar_script: Dict[str, Any]) -> str:
        """Create Tavus avatar presentation"""
        
        try:
            # Prepare presentation data for Tavus API
            presentation_data = {
                "script": avatar_script["presentation"],
                "gestures": avatar_script["gestures"],
                "timing": avatar_script["timing"],
                "metadata": {
                    "title": "AI-Powered Demo Presentation",
                    "description": "Synchronized avatar presentation with demo automation",
                    "duration": avatar_script.get("metadata", {}).get("total_duration", 300)
                }
            }
            
            # Call Tavus API to create presentation
            response = requests.post(
                f"{self.base_url}/v1/presentations",
                headers=self.headers,
                json=presentation_data
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("presentation_id", "unknown")
            else:
                raise Exception(f"Tavus API error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Error creating avatar presentation: {e}")
            return "demo_presentation_id"
    
    async def start_presentation(self, presentation_id: str) -> bool:
        """Start the avatar presentation"""
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/presentations/{presentation_id}/start",
                headers=self.headers
            )
            
            return response.status_code == 200
            
        except Exception as e:
            print(f"Error starting presentation: {e}")
            return False
    
    def generate_coordination_script(self, avatar_script: Dict[str, Any]) -> str:
        """Generate coordination script for demo automation"""
        
        coordination = avatar_script.get("demo_coordination", {})
        
        script_lines = [
            "# Demo Coordination Script",
            "# Generated by Tavus Avatar Controller",
            "",
            "import time",
            "import asyncio",
            "from typing import Dict, Any",
            "",
            "class DemoCoordinator:",
            "    def __init__(self):",
            "        self.completion_signals = {}",
            "        self.current_action = None",
            "",
            "    async def wait_for_avatar_segment(self, segment_id: str):",
            "        \"\"\"Wait for avatar to complete segment\"\"\"",
            "        # Implementation for waiting for avatar segment",
            "        pass",
            "",
            "    async def execute_demo_action(self, action_id: str):",
            "        \"\"\"Execute demo action and signal completion\"\"\"",
            "        # Implementation for demo action execution",
            "        pass",
            "",
            "    async def coordinate_presentation(self, avatar_script: Dict[str, Any]):",
            "        \"\"\"Coordinate avatar presentation with demo actions\"\"\"",
            "        coordination = avatar_script.get('demo_coordination', {})",
            "",
            "        for segment_id, demo_info in coordination.items():",
            "            # Wait for avatar to reach demo segment",
            "            await self.wait_for_avatar_segment(segment_id)",
            "",
            "            # Execute demo action",
            "            action_id = demo_info['action_id']",
            "            await self.execute_demo_action(action_id)",
            "",
            "            # Signal completion",
            "            completion_signal = demo_info['completion_signal']",
            "            self.completion_signals[completion_signal] = True",
            "",
            "            # Wait for avatar to continue",
            "            await asyncio.sleep(1)",
            "",
            "# Usage:",
            "# coordinator = DemoCoordinator()",
            "# await coordinator.coordinate_presentation(avatar_script)"
        ]
        
        return "\n".join(script_lines)

# Example usage
if __name__ == "__main__":
    # Example avatar script synthesis
    controller = TavusAvatarController("your_tavus_api_key")
    
    # Example presentation script and execution plan
    presentation_script = {
        "presentation_script": {
            "sections": [
                {
                    "title": "Introduction",
                    "duration": 30,
                    "content": "Welcome to our AI-powered demo. Let me show you how our system works.",
                    "demo_steps": ["Open the application", "Navigate to the main dashboard"]
                }
            ]
        }
    }
    
    execution_plan = {
        "demo_plan": {
            "automation_steps": [
                "Click on the login button",
                "Enter credentials",
                "Navigate to dashboard"
            ]
        }
    }
    
    # Synthesize avatar script
    avatar_script = controller.synthesize_avatar_script(presentation_script, execution_plan)
    print(json.dumps(avatar_script, indent=2)) 