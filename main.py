"""
GitIngest + LLM Integration Examples
====================================

This file demonstrates practical ways to use gitingest output with LLM calls.
The key is understanding what gitingest returns and how to structure it for LLMs.
"""

import asyncio
from gitingest import ingest, ingest_async
from datetime import datetime
import cv2
import numpy as np
from PIL import ImageGrab
import runpy
import time
from llama_chat_client import simple_chat as chat
from web_agent import record_demo

async def main(repo_url, output_file):
    print(f"📦 Running gitingest on: {repo_url}")
    print(f"📝 Output will be saved to: {output_file}")
    summary, tree, content = await ingest_async(repo_url, output=output_file)

    print(f"✅ Analysis complete!")
    print(f"📊 Summary length: {len(summary)} chars")
    print(f"🌳 Tree length: {len(tree)} chars") 
    print(f"📄 Content length: {len(content)} chars")
    
    # Key insight: gitingest returns 3 components:
    # - summary: High-level stats and info about the repo
    # - tree: Directory structure
    # - content: Full file contents
    
    # # Step 2: Basic LLM usage - Understanding the codebase
    print("\n🤖 Asking LLM about the codebase...")
    
    # Generate demo script for the repository
    demo_prompt = f"""
    Based on this repository analysis:

    SUMMARY:
    {summary}

    STRUCTURE:
    {tree}

    CONTENT:
    {content}

    Generate a step-by-step action guide for demonstrating this application's functionality. Focus on creating a list of specific actions that can be performed to showcase the app's features.

    For each demonstration step, provide:

    1. **Action**: The specific action to perform (click button, enter text, navigate to page, etc.)
    2. **Target**: What element to interact with (button name, input field, link, etc.)
    3. **Input Data**: Any specific text, values, or data to enter
    4. **Expected Outcome**: What should happen after the action

    Structure this as a numbered sequence of actions that flow logically through the application's main features. Focus on:
    - User interface interactions (clicks, inputs, selections)
    - Navigation between different parts of the app
    - Data entry and form submissions
    - Key feature demonstrations with specific examples
    - Different user workflows or scenarios

    Keep descriptions concise and action-focused. Each step should be clear enough that someone could automate it or follow it exactly.
    The script should go over each main feature of the application only once
    """
    
    response = await chat(demo_prompt)
    print("Generated Demo Script:", response)
    
    # Save demo script to file
    demo_filename = f"demo_{output_file.replace('.txt', '.md')}"
    with open(demo_filename, 'w') as f:
        f.write(response)
    print(f"💾 Demo script saved to: {demo_filename}")

    # Convert demo to Playwright script
    playwright_script = await convert_demo_to_playwright(demo_filename, summary, tree, content)
    
    # Get the output filename from convert_demo_to_playwright
    playwright_filename = demo_filename.replace('.md', '_playwright.py')
    
    # # Play and record the demo
    # print("🎥 Playing and recording demo...")
    # await play_and_record_demo(playwright_filename)

    await record_demo(response)


    # Run the demo script
    

# Utility functions for different use cases
async def ask_about_codebase(repo_path_or_url, question):
    """Simple helper to ask questions about any codebase"""
    summary, tree, content = ingest(repo_path_or_url)
    
    prompt = f"""
    Repository Analysis:
    {summary}

    Structure:
    {tree}

    Content:
    {content}

     Question: {question}
    """
    
    return await chat(prompt)

async def convert_demo_to_playwright(demo_file_path, repo_summary=None, repo_tree=None, repo_content=None):
    """Convert a demo markdown file to a Playwright script"""
    try:
        with open(demo_file_path, 'r') as f:
            demo_content = f.read()
    except FileNotFoundError:
        print(f"Demo file {demo_file_path} not found!")
        return None
    
    # Build the prompt with optional repository context
    context_section = ""
    if repo_summary and repo_tree and repo_content:
        context_section = f"""
    REPOSITORY CONTEXT:
    
    SUMMARY:
    {repo_summary}

    STRUCTURE:
    {repo_tree}

    CONTENT:
    {repo_content}
    """
    
    playwright_conversion_prompt = f"""
    Convert this step-by-step demo guide into a complete Playwright Python test script:

    DEMO CONTENT:
    {demo_content}
    {context_section}
    Generate a production-ready Playwright test that:
    1. **Imports**: Include all necessary Playwright imports
    2. **Setup**: Browser and page setup with proper configuration
    3. **Test Functions**: Convert each demo step into Playwright commands
    4. **Selectors**: Use appropriate CSS selectors for each element
    5. **Cleanup**: Proper browser and context cleanup

    Format as a complete Python file that can be run with `playwright test` or `pytest`.
    Include comments explaining each section and step.
    Focus on performing the demo actions, not validating results.
    Use the repository context to better understand the application structure and choose appropriate selectors
    Output only the Python code itself, starting directly with import statements. Do not wrap the code in markdown code blocks or any other formatting.
    Generate the code without any markdown formatting. Do not include ```python or ``` markers. Output only the raw Python code that can be saved directly to a .py file.
    Also add delays between actions to simulate human input.
    """
    
    response = await chat(playwright_conversion_prompt)

    response = response.replace("```python", "").replace("```", "")
    
    # Save the converted script
    output_filename = demo_file_path.replace('.md', '_playwright.py')
    with open(output_filename, 'w') as f:
        f.write(response)
    
    print(f"🎭 Converted demo to Playwright script: {output_filename}")
    return response

async def play_and_record_demo(demo_file_path):
    """Play and record the demo created by convert_demo_to_playwright.
    
    Args:
        demo_file_path (str): Path to the Playwright demo script file
    """
    try:
        # Initialize video writer
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"demo_recording_{timestamp}.mp4"
        
        # Take a test frame to get dimensions
        screen = ImageGrab.grab()
        frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
        height, width = frame.shape[:2]
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(output_path, fourcc, 30.0, (width, height))
        
        print("Starting demo execution and recording...")
        
        # Start recording in a separate task
        recording = True
        async def record_screen():
            try:
                while recording:
                    # Capture and write frame
                    screen = ImageGrab.grab()
                    frame = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)
                    writer.write(frame)
                    await asyncio.sleep(1/15)  # 30 FPS
            except asyncio.CancelledError:
                pass
            
        # Start recording task
        recording_task = asyncio.create_task(record_screen())
        
        try:
            # Add a small delay to ensure recording has started
            await asyncio.sleep(0.5)
            
            # Just execute the file directly
            print("Running demo script...")
            await asyncio.to_thread(exec, open(demo_file_path).read(), {'__file__': demo_file_path})
            
            # Add a small delay to capture the final state
            await asyncio.sleep(1)
            
            print("Demo completed successfully!")
        finally:
            # Stop recording
            recording = False
            await recording_task
            writer.release()
            print(f"Recording saved to {output_path}")
            
    except Exception as e:
        print(f"Error playing demo: {str(e)}")
        raise

if __name__ == "__main__":
    print("GitIngest + LLM Analysis Tool")
    print("=" * 35)
    
    # Prompt for repository URL
    repo_url = input("Enter repository URL or local path: ").strip()
    while not repo_url:
        print("Repository URL cannot be empty!")
        repo_url = input("Enter repository URL or local path: ").strip()
    
    # Prompt for output file name
    output_file = input("Enter output file name (e.g., analysis.txt): ").strip()
    while not output_file:
        print("Output file name cannot be empty!")
        output_file = input("Enter output file name (e.g., analysis.txt): ").strip()
    
    # Run the main example
    asyncio.run(main(repo_url, output_file))