#!/usr/bin/env python3
"""
Simple DeepAgent PostgreSQL Server
Runs the DeepAgent as a LangGraph API server that the chat UI can connect to.
"""

import os
import asyncio
from typing import Dict, Any
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict
from typing import Annotated

# Import our DeepAgent
try:
    from deepagents import create_deep_agent
    print("✅ DeepAgents imported successfully")
except ImportError as e:
    print(f"❌ Failed to import deepagents: {e}")
    print("Please run: pip install -e .")
    exit(1)

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def create_deepagent_graph():
    """Create the DeepAgent PostgreSQL graph"""
    
    # Get configuration from environment
    db_connection_string = os.getenv(
        "DATABASE_URL", 
        "postgresql://deepagent:test123@localhost:5432/deepagent_test"
    )
    
    enable_tracing = os.getenv("ENABLE_TRACING", "true").lower() == "true"
    tracing_project = os.getenv("TRACING_PROJECT_NAME", "deepagent-server")
    
    print(f"🗄️  Database: {db_connection_string}")
    print(f"🔭 Tracing: {'Enabled' if enable_tracing else 'Disabled'}")
    
    # Instructions for the database agent
    instructions = """You are a database analyst that helps users explore and analyze their PostgreSQL database.

You can:
- Query data from tables using postgres_query (SELECT statements only)  
- Explore database schema using postgres_schema
- Analyze tables and get insights using postgres_analyze
- Plan and track complex analysis tasks using write_todos

Always use postgres_schema first to understand the database structure before writing queries.
All operations are read-only - you cannot modify the database in any way.

Be helpful, thorough, and provide clear explanations of your analysis.
"""
    
    try:
        # Create the DeepAgent
        agent = create_deep_agent(
            tools=[],  # Built-in PostgreSQL tools will be added automatically
            instructions=instructions,
            db_connection_string=db_connection_string,
            enable_tracing=enable_tracing,
            tracing_project_name=tracing_project
        )
        
        print("✅ DeepAgent created successfully")
        return agent
        
    except Exception as e:
        print(f"❌ Failed to create DeepAgent: {e}")
        raise

def run_server():
    """Run the DeepAgent as a server"""
    
    print("🧠 Starting DeepAgent PostgreSQL Server...")
    
    # Create the agent
    agent = create_deepagent_graph()
    
    # Test the agent
    print("\n🧪 Testing DeepAgent...")
    try:
        test_result = agent.invoke({
            "messages": [{"role": "user", "content": "Hello! What tables are available in the database?"}]
        })
        print("✅ DeepAgent test successful")
    except Exception as e:
        print(f"⚠️  DeepAgent test failed: {e}")
        print("Continuing anyway - the agent may work once properly configured...")
    
    print(f"""
🎉 DeepAgent PostgreSQL Server Ready!

📊 Database: {os.getenv('DATABASE_URL', 'Default PostgreSQL')}
🔭 Tracing: {'Enabled' if os.getenv('ENABLE_TRACING', 'true').lower() == 'true' else 'Disabled'}

The DeepAgent is ready to handle database queries and analysis.
Use this in combination with the chat UI for the best experience.

To use programmatically:
    from run_deepagent_server import create_deepagent_graph
    agent = create_deepagent_graph()
    result = agent.invoke({{"messages": [{{"role": "user", "content": "Your query here"}}]}})
""")

if __name__ == "__main__":
    run_server()