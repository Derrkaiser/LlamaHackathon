#!/usr/bin/env python3
"""
Simple Avatar Presenter - Shows Tavus avatar reading scripts with natural pauses
"""

import json
import time
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class AvatarSegment:
    """Represents a segment of avatar presentation"""
    id: str
    text: str
    duration: float
    pause_after: bool = False
    gesture: str = "neutral"

class SimpleAvatarPresenter:
    """Simple avatar presenter for script reading with pauses"""
    
    def __init__(self):
        self.segments: List[AvatarSegment] = []
        self.current_segment = 0
        self.is_presenting = False
        
    def load_script(self, presentation_script: str, demo_plan: Dict[str, Any] = None):
        """Load and segment the presentation script"""
        
        self.segments = []
        
        # Split script into natural segments
        script_segments = self._split_script_into_segments(presentation_script)
        
        # Create avatar segments with timing
        for i, segment_text in enumerate(script_segments):
            # Estimate duration based on word count (average 150 words per minute)
            word_count = len(segment_text.split())
            duration = max(3.0, (word_count / 150) * 60)  # Minimum 3 seconds
            
            # Add pauses after certain segments
            pause_after = self._should_pause_after(segment_text, i, len(script_segments))
            
            # Determine gesture based on content
            gesture = self._get_gesture_for_segment(segment_text)
            
            segment = AvatarSegment(
                id=f"segment_{i+1}",
                text=segment_text.strip(),
                duration=duration,
                pause_after=pause_after,
                gesture=gesture
            )
            
            self.segments.append(segment)
    
    def _split_script_into_segments(self, script: str) -> List[str]:
        """Split script into natural speaking segments"""
        
        # Split by sentences and paragraphs
        segments = []
        
        # Split by double newlines (paragraphs)
        paragraphs = script.split('\n\n')
        
        for paragraph in paragraphs:
            if not paragraph.strip():
                continue
                
            # Split long paragraphs into sentences
            sentences = paragraph.split('. ')
            
            current_segment = ""
            for sentence in sentences:
                if not sentence.strip():
                    continue
                    
                # Add period back if it was removed
                if not sentence.endswith('.'):
                    sentence += '.'
                
                # If adding this sentence would make segment too long, start new segment
                if len(current_segment + sentence) > 200:  # Max ~200 chars per segment
                    if current_segment:
                        segments.append(current_segment.strip())
                        current_segment = sentence
                    else:
                        segments.append(sentence)
                else:
                    current_segment += " " + sentence if current_segment else sentence
            
            # Add remaining segment
            if current_segment:
                segments.append(current_segment.strip())
        
        return segments
    
    def _should_pause_after(self, segment_text: str, index: int, total_segments: int) -> bool:
        """Determine if we should pause after this segment"""
        
        text_lower = segment_text.lower()
        
        # Pause after introductions
        if any(phrase in text_lower for phrase in ['welcome', 'hello', 'thank you']):
            return True
        
        # Pause before demo sections
        if any(phrase in text_lower for phrase in ['let me show you', 'now let\'s', 'let\'s look at', 'here\'s how']):
            return True
        
        # Pause after major sections
        if any(phrase in text_lower for phrase in ['that concludes', 'in summary', 'to summarize']):
            return True
        
        # Pause every 3-4 segments for natural flow
        if (index + 1) % 3 == 0 and index < total_segments - 1:
            return True
        
        return False
    
    def _get_gesture_for_segment(self, segment_text: str) -> str:
        """Get appropriate gesture for segment content"""
        
        text_lower = segment_text.lower()
        
        if any(phrase in text_lower for phrase in ['welcome', 'hello', 'thank you']):
            return "welcome_gesture"
        elif any(phrase in text_lower for phrase in ['let me show you', 'here\'s how', 'as you can see']):
            return "point_at_screen"
        elif any(phrase in text_lower for phrase in ['important', 'key', 'critical']):
            return "emphasize_gesture"
        elif any(phrase in text_lower for phrase in ['in conclusion', 'to summarize', 'finally']):
            return "conclusion_gesture"
        else:
            return "neutral_gesture"
    
    def generate_avatar_script(self) -> Dict[str, Any]:
        """Generate the avatar script for Tavus"""
        
        avatar_segments = []
        
        for segment in self.segments:
            avatar_segments.append({
                "id": segment.id,
                "text": segment.text,
                "duration": segment.duration,
                "gesture": segment.gesture,
                "pause_after": segment.pause_after
            })
        
        return {
            "avatar_config": {
                "voice": "professional",
                "gesture_style": "natural",
                "presentation_pace": "moderate",
                "pause_duration": 2.0
            },
            "presentation": {
                "segments": avatar_segments
            },
            "timing": {
                "total_duration": sum(seg.duration for seg in self.segments),
                "segment_count": len(self.segments),
                "pause_count": sum(1 for seg in self.segments if seg.pause_after)
            }
        }
    
    def generate_embed_code(self, presentation_id: str = "demo_presentation") -> str:
        """Generate HTML embed code for Tavus player"""
        
        avatar_script = self.generate_avatar_script()
        
        return f"""
        <div id="tavus-player-container" style="width: 100%; height: 500px; border: 2px solid #667eea; border-radius: 10px; overflow: hidden; margin: 20px 0;">
            <iframe 
                src="https://app.tavus.com/embed/{presentation_id}"
                width="100%" 
                height="100%" 
                frameborder="0"
                allowfullscreen>
            </iframe>
        </div>
        
        <div id="presentation-controls" style="margin: 20px 0;">
            <button onclick="startPresentation()" style="background: #667eea; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-right: 10px;">
                🎬 Start Presentation
            </button>
            <button onclick="pausePresentation()" style="background: #f39c12; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-right: 10px;">
                ⏸️ Pause
            </button>
            <button onclick="stopPresentation()" style="background: #e74c3c; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">
                ⏹️ Stop
            </button>
        </div>
        
        <div id="presentation-status" style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
            <h4>📊 Presentation Status</h4>
            <p><strong>Total Segments:</strong> {avatar_script['timing']['segment_count']}</p>
            <p><strong>Total Duration:</strong> {avatar_script['timing']['total_duration']:.1f} seconds</p>
            <p><strong>Natural Pauses:</strong> {avatar_script['timing']['pause_count']}</p>
        </div>
        
        <script>
            // Presentation control functions
            function startPresentation() {{
                console.log('🎬 Starting avatar presentation...');
                document.getElementById('presentation-status').innerHTML += '<p style="color: green;">✅ Presentation started</p>';
                
                // Simulate segment progression
                const segments = {json.dumps(avatar_script['presentation']['segments'])};
                let currentSegment = 0;
                
                const progressInterval = setInterval(() => {{
                    if (currentSegment < segments.length) {{
                        const segment = segments[currentSegment];
                        console.log(`Segment ${{currentSegment + 1}}: ${{segment.text.substring(0, 50)}}...`);
                        
                        // Update status
                        document.getElementById('presentation-status').innerHTML += 
                            `<p style="color: #667eea;">🎭 Segment ${{currentSegment + 1}}: ${{segment.text.substring(0, 50)}}...</p>`;
                        
                        // Add pause indicator if needed
                        if (segment.pause_after) {{
                            setTimeout(() => {{
                                document.getElementById('presentation-status').innerHTML += 
                                    '<p style="color: #f39c12;">⏸️ Natural pause...</p>';
                            }}, segment.duration * 1000);
                        }}
                        
                        currentSegment++;
                    }} else {{
                        clearInterval(progressInterval);
                        document.getElementById('presentation-status').innerHTML += '<p style="color: green;">🎉 Presentation completed!</p>';
                    }}
                }}, 3000); // Update every 3 seconds for demo
            }}
            
            function pausePresentation() {{
                console.log('⏸️ Pausing presentation...');
                document.getElementById('presentation-status').innerHTML += '<p style="color: #f39c12;">⏸️ Presentation paused</p>';
            }}
            
            function stopPresentation() {{
                console.log('⏹️ Stopping presentation...');
                document.getElementById('presentation-status').innerHTML += '<p style="color: #e74c3c;">⏹️ Presentation stopped</p>';
            }}
        </script>
        """
    
    def get_presentation_summary(self) -> Dict[str, Any]:
        """Get summary of the presentation"""
        
        if not self.segments:
            return {"error": "No script loaded"}
        
        total_duration = sum(seg.duration for seg in self.segments)
        pause_count = sum(1 for seg in self.segments if seg.pause_after)
        
        return {
            "segment_count": len(self.segments),
            "total_duration": total_duration,
            "average_segment_duration": total_duration / len(self.segments),
            "pause_count": pause_count,
            "segments": [
                {
                    "id": seg.id,
                    "text_preview": seg.text[:100] + "..." if len(seg.text) > 100 else seg.text,
                    "duration": seg.duration,
                    "gesture": seg.gesture,
                    "pause_after": seg.pause_after
                }
                for seg in self.segments
            ]
        }

# Example usage
if __name__ == "__main__":
    # Test with sample script
    sample_script = """
    Welcome to our demo! Today I'm going to show you how our platform revolutionizes the way teams collaborate.
    
    Let me start by explaining the core problem we're solving. Traditional collaboration tools are fragmented and don't provide the seamless experience that modern teams need.
    
    Now, let me show you our solution. As you can see, we've created an intuitive interface that brings everything together in one place.
    
    Here's how it works. Users can create projects, assign tasks, and track progress all from a single dashboard. The system automatically syncs across all devices.
    
    Let me demonstrate the key features. First, you'll notice the clean, modern design. Everything is organized logically and easy to find.
    
    The real magic happens when you start collaborating. Team members can see updates in real-time, comment on tasks, and receive notifications instantly.
    
    In conclusion, our platform provides everything teams need to work efficiently and stay connected. Thank you for your attention!
    """
    
    presenter = SimpleAvatarPresenter()
    presenter.load_script(sample_script)
    
    print("🎭 Avatar Presentation Ready!")
    print(f"📊 Segments: {len(presenter.segments)}")
    print(f"⏱️ Total Duration: {sum(seg.duration for seg in presenter.segments):.1f} seconds")
    
    # Generate embed code
    embed_code = presenter.generate_embed_code("test_presentation")
    print("\n📋 Embed code generated successfully!")
    
    # Show summary
    summary = presenter.get_presentation_summary()
    print(f"\n📈 Summary:")
    print(f"   - Segments: {summary['segment_count']}")
    print(f"   - Duration: {summary['total_duration']:.1f}s")
    print(f"   - Pauses: {summary['pause_count']}") 