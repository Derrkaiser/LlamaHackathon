# Synchronous usage
from gitingest import ingest
import asyncio
from llama_chat_client import simple_chat as chat  # Import simplified chat function

# Basic gitingest usage
summary, tree, content = ingest("https://github.com/cyclotruc/gitingest", output="gitingest.txt")

print("Summary:")
print(summary)
print("\n" + "="*50 + "\n")

# Example 1: Use the content directly as context for LLM
async def analyze_codebase_with_llm():
    """Use gitingest output to ask questions about the codebase"""
    
    # Create a comprehensive context for the LLM
    context = f"""
    Here's a repository analysis:
    
    SUMMARY:
    {summary}
    
    FILE STRUCTURE:
    {tree}
    
    CODE CONTENT:
    {content}
    """
    
    # Ask specific questions about the codebase
    questions = [
        "What is this repository about and what are its main features?",
        "What are the key Python modules and their purposes?",
        "How would I get started using this library?",
        "What are the main dependencies and requirements?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        prompt = f"Based on this codebase information:\n{context}\n\nQuestion: {question}"
        
        try:
            response = await chat(prompt)
            print(f"Answer: {response}")
        except Exception as e:
            print(f"Error: {e}")
        
        print("-" * 50)

# Example 2: Use gitingest for code review or analysis
async def code_review_with_llm():
    """Use gitingest output for code review"""
    
    review_prompt = f"""
    Please review this codebase and provide insights:
    
    Repository Summary: {summary}
    
    File Structure: {tree}
    
    Key files content: {content}
    
    Please provide:
    1. Overall code quality assessment
    2. Architecture observations
    3. Potential improvements
    4. Security considerations
    5. Documentation quality
    """
    
    try:
        response = await chat(review_prompt)
        print("Code Review Results:")
        print(response)
    except Exception as e:
        print(f"Error during code review: {e}")

# Example 3: Generate documentation from codebase
async def generate_docs_with_llm():
    """Generate documentation using gitingest output"""
    
    docs_prompt = f"""
    Based on this codebase analysis, generate comprehensive documentation:
    
    Summary: {summary}
    Structure: {tree}
    Content: {content}
    
    Please create:
    1. A clear README section explaining what this does
    2. Installation instructions
    3. Usage examples
    4. API documentation for key functions
    5. Contributing guidelines
    """
    
    try:
        response = await chat(docs_prompt)
        print("Generated Documentation:")
        print(response)
        
        # Optionally save to file
        with open("generated_docs.md", "w") as f:
            f.write(response)
        print("\nDocumentation saved to generated_docs.md")
        
    except Exception as e:
        print(f"Error generating docs: {e}")

# Example 4: Smart code search and explanation
async def search_and_explain_code():
    """Use LLM to search and explain specific code patterns"""
    
    search_queries = [
        "How does the ingestion process work?",
        "What are the main configuration options?",
        "How are files processed and filtered?",
        "What output formats are supported?"
    ]
    
    for query in search_queries:
        prompt = f"""
        Based on this codebase:
        
                 Summary: {summary}
         File Structure: {tree}
         Content: {content}
         
         Please answer: {query}
        
        Provide specific code examples and explanations where relevant.
        """
        
        try:
            response = await chat(prompt)
            print(f"\nQuery: {query}")
            print(f"Response: {response}")
            print("-" * 50)
        except Exception as e:
            print(f"Error: {e}")

# Run the examples
if __name__ == "__main__":
    print("Running GitIngest + LLM Analysis Examples...")
    
    # Uncomment the example you want to run:
    # asyncio.run(analyze_codebase_with_llm())
    # asyncio.run(code_review_with_llm())
    # asyncio.run(generate_docs_with_llm())
    # asyncio.run(search_and_explain_code())
    
    # Or run all examples:
    async def run_all_examples():
        print("\n1. Analyzing codebase...")
        await analyze_codebase_with_llm()
        
        print("\n2. Performing code review...")
        await code_review_with_llm()
        
        print("\n3. Generating documentation...")
        await generate_docs_with_llm()
        
        print("\n4. Searching and explaining code...")
        await search_and_explain_code()
    
    # asyncio.run(run_all_examples())
