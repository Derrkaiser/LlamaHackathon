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
                
                # If we weren't writing before, flush any buffered frames and start writing
                if not self.is_currently_writing:
                    self.is_currently_writing = True
                    # Write all buffered frames first
                    for buffered_frame in self.frames_buffer:
                        self.writer.write(buffered_frame)
                    self.frames_buffer.clear()
        
        # Determine if we should be writing or buffering
        time_since_activity = time.time() - self.last_activity_time
        
        if self.is_currently_writing:
            if time_since_activity <= self.max_inactive_seconds:
                # Continue writing - there's been recent activity
                self.writer.write(frame)
            else:
                # Stop writing and start buffering - no activity for too long
                self.is_currently_writing = False
                self.frames_buffer = [frame]  # Start new buffer
        else:
            # We're buffering - add frame to buffer but limit buffer size
            self.frames_buffer.append(frame)
            # Keep only the last 2 seconds worth of frames in buffer
            max_buffer_size = int(self.fps * self.max_inactive_seconds)
            if len(self.frames_buffer) > max_buffer_size:
                self.frames_buffer.pop(0)
        
        self.last_frame = frame.copy()

async def main() -> None:
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

    # # Task description
    # detailed_task = """
    # Complete the following task step by step:
    # 1. Navigate to https://javascriptbear.github.io/todo_react_app/
    # 2. Wait for the page to fully load
    # 3. Look for and click on the 'Create New Task' button (or similar button to add a new task)
    # 4. Fill in the task title field with 'Buy groceries'
    # 5. Fill in the task summary/description field with 'Buy milk, eggs, and bread'
    # 6. Submit/save the new task by clicking the appropriate save/submit button
    # 7. Verify that the task was created successfully by checking if it appears in the task list
    
    # Make sure to complete ALL steps. If any step fails, try different approaches until successful.
    # The task is only complete when you have successfully created and can see the new task in the list.
    # """

    detailed_task = """
    1. Open the Todo React App at https://javascriptbear.github.io/todo_react_app/
2. Click the "New Task" button to create a new task
3. Enter a task title and summary, then click "Create Task"
4. View the newly created task in the list
5. Click the trash icon next to a task to delete it
7. Refresh the page to verify that tasks are persisted in local storage
"""

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

asyncio.run(main())




# import json
# from dataclasses import dataclass
# from typing import List

# from autogen_core import (
#     FunctionCall,
#     MessageContext,
#     RoutedAgent,
#     message_handler,
# )
# from autogen_core.model_context import ChatCompletionContext
# from autogen_core.models import (
#     AssistantMessage,
#     ChatCompletionClient,
#     FunctionExecutionResult,
#     FunctionExecutionResultMessage,
#     LLMMessage,
#     SystemMessage,
#     UserMessage,
# )
# from autogen_core.tools import ToolResult, Workbench
# @dataclass
# class Message:
#     content: str


# class WorkbenchAgent(RoutedAgent):
#     def __init__(
#         self, model_client: ChatCompletionClient, model_context: ChatCompletionContext, workbench: Workbench
#     ) -> None:
#         super().__init__("An agent with a workbench")
#         self._system_messages: List[LLMMessage] = [SystemMessage(content="""
                                                                 
# You are a helpful assistant and an expert in function composition. You can answer general questions using your internal knowledge OR invoke functions when necessary. Follow these strict guidelines:

# 1. FUNCTION CALLS:
# - ONLY use functions that are EXPLICITLY listed in the function list below
# - If NO functions are listed (empty function list []), respond ONLY with internal knowledge or "I don't have access to [Unavailable service] information"
# - If a function is not in the list, respond ONLY with internal knowledge or "I don't have access to [Unavailable service] information"
# - If ALL required parameters are present AND the query EXACTLY matches a listed function's purpose: output ONLY the function call(s)
# - Use exact format: [{"name": "<tool_name_foo>","parameters": {"<param1_name>": "<param1_value>","<param2_name>": "<param2_value>"}}]
# Examples:
# CORRECT: [{"name": "get_weather","parameters": {"location": "Vancouver"}},{"name": "calculate_route","parameters": {"start": "Boston","end": "New York"}}] <- Only if get_weather and calculate_route are in function list

# INCORRECT: [{"name": "population_projections", "parameters": {"country": "United States", "years": 20}}]] <- Bad json format
# INCORRECT: Let me check the weather: [{"name": "get_weather","parameters": {"location": "Vancouver"}}]
# INCORRECT: [{"name": "get_events","parameters": {"location": "Singapore"}}] <- If function not in list
                                                                 
#                                                                  DO NOT OUTPUT <|python_end|><|header_start|>assistant<|header_end|>

# 2. RESPONSE RULES:
# - For pure function requests matching a listed function: ONLY output the function call(s)
# - For knowledge questions: ONLY output text
# - For missing parameters: ONLY request the specific missing parameters
# - For unavailable services (not in function list): output ONLY with internal knowledge or "I don't have access to [Unavailable service] information". Do NOT execute a function call.
# - If the query asks for information beyond what a listed function provides: output ONLY with internal knowledge about your limitations
# - NEVER combine text and function calls in the same response
# - NEVER suggest alternative functions when the requested service is unavailable
# - NEVER create or invent new functions not listed below

# 3. STRICT BOUNDARIES:
# - ONLY use functions from the list below - no exceptions
# - NEVER use a function as an alternative to unavailable information
# - NEVER call functions not present in the function list
# - NEVER add explanatory text to function calls
# - NEVER respond with empty brackets
# - Use proper Python/JSON syntax for function calls
# - Check the function list carefully before responding

# 4. TOOL RESPONSE HANDLING:
# - When receiving tool responses: provide concise, natural language responses
# - Don't repeat tool response verbatim
# - Don't add supplementary information

# """)]
#         self._model_client = model_client
#         self._model_context = model_context
#         self._workbench = workbench

#     @message_handler
#     async def handle_user_message(self, message: Message, ctx: MessageContext) -> Message:
#         # Add the user message to the model context.
#         await self._model_context.add_message(UserMessage(content=message.content, source="user"))
#         # print("---------User Message-----------")
#         # print(message.content)

#         # Run the chat completion with the tools.
#         create_result = await self._model_client.create(
#             messages=self._system_messages + (await self._model_context.get_messages()),
#             tools=(await self._workbench.list_tools()),
#             cancellation_token=ctx.cancellation_token,
#         )

#         # Run tool call loop.
#         while isinstance(create_result.content, list) and all(
#             isinstance(call, FunctionCall) for call in create_result.content
#         ):
#             print("---------Function Calls-----------")
#             for call in create_result.content:
#                 print(call)

#             # Add the function calls to the model context.
#             await self._model_context.add_message(AssistantMessage(content=create_result.content, source="assistant"))

#             # Call the tools using the workbench.
#             print("---------Function Call Results-----------")
#             results: List[ToolResult] = []
#             for call in create_result.content:
#                 result = await self._workbench.call_tool(
#                     call.name, arguments=json.loads(call.arguments), cancellation_token=ctx.cancellation_token
#                 )
#                 results.append(result)
#                 print(result)

#             # Add the function execution results to the model context.
#             await self._model_context.add_message(
#                 FunctionExecutionResultMessage(
#                     content=[
#                         FunctionExecutionResult(
#                             call_id=call.id,
#                             content=result.to_text(),
#                             is_error=result.is_error,
#                             name=result.name,
#                         )
#                         for call, result in zip(create_result.content, results, strict=False)
#                     ]
#                 )
#             )

#             # Run the chat completion again to reflect on the history and function execution results.
#             create_result = await self._model_client.create(
#                 messages=self._system_messages + (await self._model_context.get_messages()),
#                 tools=(await self._workbench.list_tools()),
#                 cancellation_token=ctx.cancellation_token,
#             )

#         # Now we have a single message as the result.
#         assert isinstance(create_result.content, str)

#         print("---------Final Response-----------")
#         print(create_result.content)

#         # Add the assistant message to the model context.
#         await self._model_context.add_message(AssistantMessage(content=create_result.content, source="assistant"))

#         # Return the result as a message.
#         return Message(content=create_result.content)

# from autogen_core import AgentId, SingleThreadedAgentRuntime
# from autogen_core.model_context import BufferedChatCompletionContext
# from autogen_ext.models.openai import OpenAIChatCompletionClient
# from autogen_ext.tools.mcp import McpWorkbench, SseServerParams, StreamableHttpServerParams

# async def main():
#     # playwright_server_params = StreamableHttpServerParams(
#     #     url="http://localhost:8931/mcp",
#     # )

#     playwright_server_params = SseServerParams(
#         url="http://localhost:8931/sse",
#     )

#     detailed_task = """
    
#     Complete the following task step by step:
#     1. Navigate to https://javascriptbear.github.io/todo_react_app/
#     2. Wait for the page to fully load
#     3. Look for and click on the 'Create New Task' button (or similar button to add a new task)
#     4. Fill in the task title field with 'Buy groceries'
#     5. Fill in the task summary/description field with 'Buy milk, eggs, and bread twice'
#     6. Submit/save the new task by clicking the appropriate save/submit button
#     7. Verify that the task was created successfully by checking if it appears in the task list
    
#     Make sure to complete ALL steps. If any step fails, try different approaches until successful.
#     The task is only complete when you have successfully created and can see the new task in the list.
#     """

#     # Start the workbench in a context manager.
#     # You can also start and stop the workbench using `workbench.start()` and `workbench.stop()`.
#     async with McpWorkbench(playwright_server_params) as workbench:  # type: ignore
#         # Create a single-threaded agent runtime.
#         runtime = SingleThreadedAgentRuntime()

#         # Register the agent with the runtime.
#         await WorkbenchAgent.register(
#             runtime=runtime,
#             type="WebAgent",
#             factory=lambda: WorkbenchAgent(
#                 model_client=OpenAIChatCompletionClient(
#                     model="Llama-4-Maverick-17B-128E-Instruct-FP8",  # Maverick seems to have better compatibility
#                     api_key="LLM|1237290154055733|H7Y_BoRWw3RMU2TDMqdeJT28M4Q",
#                     base_url="https://api.llama.com/compat/v1/",
#                     model_info=ModelInfo(vision=True, function_calling=True, json_output=True, family="llama-4-maverick", structured_output=True),
#                 ),
#                 model_context=BufferedChatCompletionContext(buffer_size=10),
#                 workbench=workbench,
#             ),
#         )

#         # Start the runtime.
#         runtime.start()

#         # Send a message to the agent.
#         await runtime.send_message(
#             Message(content=detailed_task),
#             recipient=AgentId("WebAgent", "default"),
#         )

#         # Stop the runtime.
#         await runtime.stop()

# asyncio.run(main())


# Autonomously complete a coding task:
# import asyncio
# from autogen_ext.models.openai import OpenAIChatCompletionClient
# from autogen_ext.teams.magentic_one import MagenticOne
# from autogen_agentchat.ui import Console


# async def example_usage():

#     detailed_task = """
#     Complete the following task step by step:
#     1. Navigate to https://javascriptbear.github.io/todo_react_app/
#     2. Wait for the page to fully load
#     3. Look for and click on the 'Create New Task' button (or similar button to add a new task)
#     4. Fill in the task title field with 'Buy groceries'
#     5. Fill in the task summary/description field with 'Buy milk, eggs, and bread twice'
#     6. Submit/save the new task by clicking the appropriate save/submit button
#     7. Verify that the task was created successfully by checking if it appears in the task list
    
#     Make sure to complete ALL steps. If any step fails, try different approaches until successful.
#     The task is only complete when you have successfully created and can see the new task in the list.
#     """
#     client = OpenAIChatCompletionClient(
#         model="Llama-4-Scout-17B-16E-Instruct-FP8",
#         api_key="LLM|1237290154055733|H7Y_BoRWw3RMU2TDMqdeJT28M4Q",
#         base_url="https://api.llama.com/compat/v1/",
#         model_info=ModelInfo(vision=True, function_calling=True, json_output=True, family="unknown", structured_output=True),
#     )  
#     m1 = MagenticOne(client=client)
#     task = detailed_task
#     result = await Console(m1.run_stream(task=task))
#     print(result)


# if __name__ == "__main__":
#     asyncio.run(example_usage())


# import asyncio
# from autogen_agentchat.ui import Console
# from autogen_agentchat.teams import RoundRobinGroupChat
# from autogen_ext.models.openai import OpenAIChatCompletionClient
# from autogen_ext.agents.web_surfer import MultimodalWebSurfer


# async def main() -> None:
#     # Define an agent
#     web_surfer_agent = MultimodalWebSurfer(
#         name="MultimodalWebSurfer",
#         model_client=OpenAIChatCompletionClient(
#             model="Llama-4-Scout-17B-16E-Instruct-FP8",
#             api_key="LLM|1237290154055733|H7Y_BoRWw3RMU2TDMqdeJT28M4Q",
#             base_url="https://api.llama.com/compat/v1/",
#             model_info=ModelInfo(vision=True, function_calling=True, json_output=True, family="llama-4-scout", structured_output=True),
#         ),
#     )

#     # Define a team
#     agent_team = RoundRobinGroupChat([web_surfer_agent], max_turns=3)

#     # Run the team and stream messages to the console
#     stream = agent_team.run_stream(task="Navigate to the AutoGen readme on GitHub.")
#     await Console(stream)
#     # Close the browser controlled by the agent
#     await web_surfer_agent.close()


# asyncio.run(main())
