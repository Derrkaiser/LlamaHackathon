import nest_asyncio
import json
import os
from llama_api_client import AsyncLlamaAPIClient
from mcp_clients.playwright_mcp_client import PlaywrightMCPClient
from dotenv import load_dotenv

load_dotenv()

# load credentials from .env file
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")
PLAYWRIGHT_URL = os.getenv("PLAYWRIGHT_URL")

client = AsyncLlamaAPIClient(api_key=LLAMA_API_KEY)

# allows async functions to run in jupyter notebook
nest_asyncio.apply()

# initialize the Gmail MCP client
playwright_mcp_client = PlaywrightMCPClient()

# chat function
async def chat(user_input):
    """
    Processes user input through a two-step LLM interaction with tool integration.

    This function performs the following steps:
    1. Connects to Gmail MCP server and retrieves available tools (only if not already connected)
    2. Makes initial LLM call to determine which tool to use
    3. Executes the selected tool with provided arguments
    4. Makes second LLM call to generate final response based on tool output

    Args:
        user_input (str): The input message from the user to be processed

    Returns:
        str: The final response message from the LLM

    Raises:
        None
    """

    # get tools from Zapier server - only connect if not already connected
    if not playwright_mcp_client.session:
        await playwright_mcp_client.connect_to_server(PLAYWRIGHT_URL)
    tools = await playwright_mcp_client.get_tools()    

    # 1st LLM call to determine which tool to use
    response = await client.chat.completions.create(
        model="Llama-4-Maverick-17B-128E-Instruct-FP8",  # Using cheaper model to avoid quota issues
        messages=[{"role": "user", "content": user_input}],
        tools=tools
    )

    # if LLM decides to use a tool
    if response.choices[0].message.tool_calls:        
        tool_name = response.choices[0].message.tool_calls[0].function.name
        tool_args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        print(f"Tool Used: {tool_name}, Arguments: {tool_args}")

        # execute the tool called by the LLM
        tool_response = await playwright_mcp_client.session.call_tool(tool_name, tool_args)
        tool_response_text = tool_response.content[0].text    

        # 2nd LLM call to determine final response
        res = await client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct-FP8",  # Using cheaper model to avoid quota issues
            messages=[
                {"role": "user", "content": user_input},
                {"role": "function", "name": tool_name, "content": tool_response_text},
            ]        
        )

        response = res.choices[0].message.content
        
    # if LLM decides not to use a tool
    else:
        response = response.choices[0].message.content

    await playwright_mcp_client.disconnect()
    
    return response    

async def close_browser():
    """
    Manually close the browser session when you're done with all tasks.
    Call this when you want to clean up resources.
    """
    if playwright_mcp_client.session:
        await playwright_mcp_client.disconnect()
        print("Browser session closed.")
    else:
        print("No active browser session to close.")


