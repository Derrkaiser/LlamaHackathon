import os
import asyncio
from llama_api_client import AsyncLlamaAPIClient
from dotenv import load_dotenv

load_dotenv()

class LlamaChatClient:
    """
    Simple class for making chat completions using the Llama SDK.
    Provides both sync and async methods for flexibility.
    """
    
    def __init__(self, api_key=None, model="Llama-4-Maverick-17B-128E-Instruct-FP8"):
        """
        Initialize the Llama chat client.
        
        Args:
            api_key (str, optional): Llama API key. If None, will use LLAMA_API_KEY from environment.
            model (str): Model name to use for completions.
        """
        self.api_key = api_key or os.getenv("LLAMA_API_KEY")
        self.model = model
        self.client = AsyncLlamaAPIClient(api_key=self.api_key)
    
    async def chat_async(self, message, system_prompt=None):
        """
        Make an async chat completion request.
        
        Args:
            message (str): User message to send
            system_prompt (str, optional): System prompt to set context
            
        Returns:
            str: Response content from the model
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": message})
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            
            # Extract the text content from the response
            if hasattr(response, 'choices') and len(response.choices) > 0:
                choice = response.choices[0]
                if hasattr(choice, 'message') and hasattr(choice.message, 'content'):
                    return choice.message.content
            
            # If response structure is different, try to extract content
            if hasattr(response, 'completion_message'):
                completion = response.completion_message
                if hasattr(completion, 'content'):
                    content = completion.content
                    if hasattr(content, 'text'):
                        return content.text
                    elif isinstance(content, str):
                        return content
            
            # Fallback: return the full response if we can't extract content
            return str(response)
            
        except Exception as e:
            return f"Error making chat request: {str(e)}"
    
    def chat(self, message, system_prompt=None):
        """
        Make a synchronous chat completion request.
        
        Args:
            message (str): User message to send
            system_prompt (str, optional): System prompt to set context
            
        Returns:
            str: Response content from the model
        """
        return asyncio.run(self.chat_async(message, system_prompt))


# Create a default instance for easy importing
default_client = LlamaChatClient()

# Convenience functions that match the expected simple_chat interface
async def simple_chat(message, system_prompt=None):
    """
    Simple async chat function that matches the expected interface.
    
    Args:
        message (str): User message to send
        system_prompt (str, optional): System prompt to set context
        
    Returns:
        str: Response content from the model
    """
    return await default_client.chat_async(message, system_prompt)

def simple_chat_sync(message, system_prompt=None):
    """
    Simple synchronous chat function.
    
    Args:
        message (str): User message to send
        system_prompt (str, optional): System prompt to set context
        
    Returns:
        str: Response content from the model
    """
    return default_client.chat(message, system_prompt)

# For debugging - handle different response structures
def debug_response(response):
    """
    Debug function to understand response structure.
    
    Args:
        response: The raw response from the API
        
    Returns:
        str: Formatted debug information
    """
    debug_info = []
    debug_info.append(f"Response type: {type(response)}")
    debug_info.append(f"Response attributes: {dir(response)}")
    
    if hasattr(response, '__dict__'):
        debug_info.append(f"Response dict: {response.__dict__}")
    
    return "\n".join(debug_info) 