#!/usr/bin/env python3
"""
Example of using deepagent with PostgreSQL database tools.

This example demonstrates how to create and use a deepagent that connects to a PostgreSQL database
instead of using the mock file system.
"""

import os
from deepagents import create_deep_agent


def main():
    # Database connection string - modify this to match your PostgreSQL setup
    # Format: postgresql://username:password@host:port/database_name
    db_connection_string = os.getenv(
        "DATABASE_URL", 
        "postgresql://username:password@localhost:5432/your_database"
    )
    
    # Additional instructions for the agent
    instructions = """You are a database analyst that helps users explore and analyze their PostgreSQL database.
    
    You can:
    - Query data from tables using postgres_query (SELECT statements only)
    - Explore database schema using postgres_schema
    - Analyze tables and get insights using postgres_analyze
    - Plan and track complex analysis tasks using write_todos
    
    Always use postgres_schema first to understand the database structure before writing queries.
    All operations are read-only - you cannot modify the database in any way.
    """
    
    # Create the deep agent with PostgreSQL tools
    agent = create_deep_agent(
        tools=[],  # No additional tools needed for this example
        instructions=instructions,
        db_connection_string=db_connection_string
    )
    
    print("PostgreSQL DeepAgent initialized!")
    print(f"Connected to database: {db_connection_string}")
    print("\nExample usage:")
    print("1. Ask 'Show me all tables' to see available tables")
    print("2. Ask 'Show me the schema for table_name' to see table structure")
    print("3. Ask 'Query the users table' to retrieve data")
    print("4. Ask 'Analyze the users table' to get insights and statistics")
    print("5. Ask 'Show me the database overview' to see all tables and sizes")
    
    # Example interaction
    try:
        # Show available tables
        response = agent.invoke("Show me all available tables in the database")
        print("\n" + "="*50)
        print("AGENT RESPONSE:")
        print("="*50)
        for message in response.get("messages", []):
            if hasattr(message, 'content'):
                print(message.content)
    
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure your PostgreSQL database is running and the connection string is correct!")
        print("Set the DATABASE_URL environment variable with your connection string.")


if __name__ == "__main__":
    main()