#!/usr/bin/env python3
"""
Chat interface for DeepAgent PostgreSQL + Phoenix tracing.
This script is called by the LangGraph chat UI to process user queries.
"""

import os
import sys
import json
import asyncio
from typing import Dict, Any

# Add the src directory to the path to import deepagents
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.dirname(__file__))

from deepagents import create_deep_agent


async def process_query(query: str, config: Dict[str, Any]) -> str:
    """Process a user query using DeepAgent."""
    try:
        # Extract configuration
        db_connection_string = config.get('databaseUrl', 'postgresql://deepagent:test123@localhost:5432/deepagent_test')
        enable_tracing = config.get('enableTracing', True)
        tracing_project_name = config.get('tracingProjectName', 'deepagent-chat-ui')
        
        # Database analyst instructions
        instructions = """You are a PostgreSQL database analyst that helps users explore and analyze their database.

You can:
- Query data from tables using postgres_query (SELECT statements only)
- Explore database schema using postgres_schema
- Analyze tables and get insights using postgres_analyze
- Plan and track complex analysis tasks using write_todos

Always use postgres_schema first to understand the database structure before writing queries.
All operations are read-only - you cannot modify the database in any way.
Provide clear, actionable insights and format your responses in a user-friendly way.
"""
        
        # Create the DeepAgent
        agent = create_deep_agent(
            tools=[],  # Using built-in PostgreSQL tools
            instructions=instructions,
            db_connection_string=db_connection_string,
            enable_tracing=enable_tracing,
            tracing_project_name=tracing_project_name
        )
        
        # Process the query
        result = agent.invoke({
            "messages": [{"role": "user", "content": query}]
        })
        
        # Extract the response from the result
        if "messages" in result and result["messages"]:
            last_message = result["messages"][-1]
            if hasattr(last_message, 'content'):
                return last_message.content
            else:
                return str(last_message)
        else:
            return "I processed your request, but didn't generate a response. Please try rephrasing your question."
            
    except Exception as e:
        error_msg = f"Error processing query: {str(e)}"
        print(error_msg, file=sys.stderr)
        return f"I encountered an error while processing your request: {str(e)}. Please check that the PostgreSQL database is running and accessible."


def main():
    """Main entry point for the chat interface."""
    try:
        # Read input from stdin
        input_data = sys.stdin.read()
        if not input_data.strip():
            print("No input provided", file=sys.stderr)
            sys.exit(1)
            
        # Parse the JSON input
        data = json.loads(input_data)
        query = data.get('query', '')
        config = data.get('config', {})
        
        if not query:
            print("No query provided", file=sys.stderr)
            sys.exit(1)
        
        # Process the query
        response = asyncio.run(process_query(query, config))
        
        # Output the response
        print(response)
        
    except json.JSONDecodeError as e:
        print(f"Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()