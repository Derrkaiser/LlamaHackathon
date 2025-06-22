# # pip install -U autogen-agentchat autogen-ext[openai,web-surfer]
# # playwright install
import asyncio
import os
import time
from datetime import datetime
from autogen_agentchat.agents import UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat, MagenticOneGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_core.models import ModelInfo

# Optional: Import for screen recording
try:
    import cv2
    import numpy as np
    from PIL import ImageGrab
    RECORDING_AVAILABLE = True
except ImportError:
    RECORDING_AVAILABLE = False

class ActivityRecorder:
    def __init__(self, output_path="task_recording.mp4", fps=30, activity_threshold=0.01, max_inactive_seconds=3):
        self.output_path = output_path
        self.fps = fps
        self.activity_threshold = activity_threshold
        self.max_inactive_seconds = max_inactive_seconds
        self.writer = None
        self.last_frame = None
        self.recording = False
        self.frames_buffer = []
        self.last_activity_time = time.time()
        self.is_currently_writing = False
        
    def start_recording(self):
        if not RECORDING_AVAILABLE:
            print("Recording not available - missing dependencies")
            return
        self.recording = True
        self.last_activity_time = time.time()
        self.is_currently_writing = True
        
    def stop_recording(self):
        self.recording = False
        if self.writer:
            # Write any remaining buffered frames
            for frame in self.frames_buffer:
                self.writer.write(frame)
            self.frames_buffer.clear()
            self.writer.release()
            print(f"Recording saved to {self.output_path}")
        
    def capture_frame(self):
        if not self.recording or not RECORDING_AVAILABLE:
            return
            
        # Capture screen
        screen = ImageGrab.grab()
        frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        
        # Initialize writer if needed
        if self.writer is None:
            height, width = frame.shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.writer = cv2.VideoWriter(self.output_path, fourcc, self.fps, (width, height))
        
        # Check for activity (frame difference)
        activity_detected = False
        if self.last_frame is not None:
            diff = cv2.absdiff(frame, self.last_frame)
            activity_score = np.mean(diff) / 255.0
            if activity_score > self.activity_threshold:
                activity_detected = True
                self.last_activity_time = time.time()
                
                # If we weren't writing before, write all buffered frames
                if not self.is_currently_writing:
                    self.is_currently_writing = True
                    # Write all buffered frames in chronological order
                    if self.frames_buffer:
                        print(f"Activity detected - writing {len(self.frames_buffer)} buffered frames")
                        for buffered_frame in self.frames_buffer:
                            self.writer.write(buffered_frame)
                        self.frames_buffer.clear()
        
        # Determine if we should be writing or buffering
        time_since_activity = time.time() - self.last_activity_time
        
        if activity_detected or (self.is_currently_writing and time_since_activity <= self.max_inactive_seconds):
            # Write the current frame immediately if there's activity or we're in an active period
            self.writer.write(frame)
        else:
            # Switch to buffering mode if we've been inactive
            if self.is_currently_writing:
                self.is_currently_writing = False
                self.frames_buffer = []
            
            # Add frame to buffer with size limit
            self.frames_buffer.append(frame)
            max_buffer_size = int(self.fps * self.max_inactive_seconds)
            if len(self.frames_buffer) > max_buffer_size:
                self.frames_buffer.pop(0)
        
        self.last_frame = frame.copy()

async def record_demo(task) -> None:
    model_client = OpenAIChatCompletionClient(
        model="Llama-4-Scout-17B-16E-Instruct-FP8",
        api_key="LLM|1237290154055733|H7Y_BoRWw3RMU2TDMqdeJT28M4Q",
        base_url="https://api.llama.com/compat/v1/",
        model_info=ModelInfo(vision=True, function_calling=True, json_output=True, family="llama-4-scout", structured_output=True),
    )  
    
    # Configure web surfer for optimal recording (faster execution, less waiting)
    web_surfer = MultimodalWebSurfer(
        "web_surfer", 
        model_client, 
        headless=False, 
        animate_actions=True,
     
    )
    
    
    # Add termination condition to stop when task is completed
    # Use a single key phrase that we know appears in the completion message
    termination = TextMentionTermination("I've successfully completed the task. Here's a summary of the steps taken:")
    
    # Use MagenticOneGroupChat for autonomous execution
    team = MagenticOneGroupChat([web_surfer], termination_condition=termination, model_client=model_client)


    detailed_task = task

    # Initialize recorder
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    recorder = ActivityRecorder(f"todo_task_recording_{timestamp}.mp4")
    
    try:
        # Start recording
        recorder.start_recording()
        print("Starting task execution and recording...")
        
        # Create a recording task that runs alongside the main task
        async def recording_loop():
            while recorder.recording:
                recorder.capture_frame()
                await asyncio.sleep(1/30)  # 30 FPS
        
        # Run both the main task and recording concurrently
        if RECORDING_AVAILABLE:
            await asyncio.gather(
                Console(team.run_stream(task=detailed_task)),
                recording_loop()
            )
        else:
            await Console(team.run_stream(task=detailed_task))

        print("Task completed successfully!")
        

    finally:
        recorder.stop_recording()
        await web_surfer.close()
        await model_client.close()
