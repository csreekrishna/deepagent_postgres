"""Test script for Phoenix tracing with DeepAgent PostgreSQL."""

import os
from deepagents import create_deep_agent
from deepagents.tracing import start_phoenix_server, get_phoenix_url

def test_phoenix_tracing():
    """Test DeepAgent with Phoenix tracing enabled."""
    
    # Start Phoenix server
    print("Starting Phoenix server...")
    start_phoenix_server()
    
    # Database connection string
    db_connection_string = os.getenv(
        "DATABASE_URL", 
        "postgresql://deepagent:test123@localhost:5432/deepagent_test"
    )
    
    # Instructions for the database agent
    instructions = """You are a database analyst that helps users explore and analyze their PostgreSQL database.

You can:
- Query data from tables using postgres_query (SELECT statements only)
- Explore database schema using postgres_schema
- Analyze tables and get insights using postgres_analyze
- Plan and track complex analysis tasks using write_todos

Always use postgres_schema first to understand the database structure before writing queries.
All operations are read-only - you cannot modify the database in any way.
"""
    
    # Create the agent with Phoenix tracing enabled
    print("Creating DeepAgent with Phoenix tracing...")
    agent = create_deep_agent(
        tools=[],
        instructions=instructions,
        db_connection_string=db_connection_string,
        enable_tracing=True,
        tracing_project_name="deepagent-test"
    )
    
    # Test queries
    test_queries = [
        "Show me all tables in the database",
        "Get the schema for the users table",
        "Show me the first 5 users from the users table",
        "Analyze the orders table and show me key statistics"
    ]
    
    print(f"\nPhoenix dashboard available at: {get_phoenix_url()}")
    print("\nRunning test queries...")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"Test Query {i}: {query}")
        print('='*60)
        
        try:
            result = agent.invoke({
                "messages": [{"role": "user", "content": query}]
            })
            
            # Print the response
            if "messages" in result and result["messages"]:
                last_message = result["messages"][-1]
                if hasattr(last_message, 'content'):
                    print(last_message.content)
                else:
                    print(str(last_message))
            else:
                print("No response received")
                
        except Exception as e:
            print(f"Error: {str(e)}")
    
    print(f"\n{'='*60}")
    print("Test completed!")
    print(f"View detailed traces at: {get_phoenix_url()}")
    print('='*60)

if __name__ == "__main__":
    test_phoenix_tracing()