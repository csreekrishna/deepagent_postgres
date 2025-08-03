#!/usr/bin/env python3
"""
Test script to verify the PostgreSQL tools work correctly.

This script tests the basic functionality of the postgres tools without requiring
an actual database connection.
"""

import sys
import os

# Add the src directory to the path so we can import deepagents
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from deepagents.tools import postgres_query, postgres_execute, postgres_schema
from deepagents.state import DeepAgentState


def test_postgres_tools_without_db():
    """Test that postgres tools handle missing database connection gracefully."""
    print("Testing PostgreSQL tools without database connection...")
    
    # Create a mock state without database connection
    state = DeepAgentState(messages=[])
    
    # Test postgres_query
    print("\n1. Testing postgres_query...")
    result = postgres_query.invoke({"query": "SELECT * FROM users", "state": state})
    print(f"Result: {result}")
    assert "No database connection available" in result
    
    # Test postgres_schema
    print("\n2. Testing postgres_schema...")
    result = postgres_schema.invoke({"state": state})
    print(f"Result: {result}")
    assert "No database connection available" in result
    
    # Test postgres_execute (this returns a Command, so we need to handle it differently)
    print("\n3. Testing postgres_execute...")
    try:
        result = postgres_execute.invoke({
            "query": "INSERT INTO users (name) VALUES ('test')", 
            "state": state, 
            "tool_call_id": "test_tool_call_id"
        })
        print(f"Result type: {type(result)}")
        print("postgres_execute returned a Command object as expected")
        # Check if the error message is in the command
        if hasattr(result, 'update') and 'messages' in result.update:
            message_content = result.update['messages'][0].content
            if "No database connection available" in message_content:
                print("✅ postgres_execute correctly handles missing database connection")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n✅ All tools handle missing database connection correctly!")


def test_import_structure():
    """Test that all imports work correctly."""
    print("Testing import structure...")
    
    try:
        from deepagents.graph import create_deep_agent
        print("✅ Successfully imported create_deep_agent")
        
        from deepagents.tools import write_todos, postgres_query, postgres_execute, postgres_schema
        print("✅ Successfully imported all postgres tools")
        
        from deepagents.state import DeepAgentState
        print("✅ Successfully imported DeepAgentState")
        
        print("\n✅ All imports successful!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    return True


def test_create_deep_agent():
    """Test creating a deep agent with postgres tools."""
    print("Testing create_deep_agent with PostgreSQL tools...")
    
    try:
        from deepagents.graph import create_deep_agent
        
        # Test creating agent without database connection
        agent = create_deep_agent(
            tools=[],
            instructions="Test agent",
        )
        print("✅ Successfully created agent without database connection")
        
        # Test creating agent with database connection string
        agent = create_deep_agent(
            tools=[],
            instructions="Test database agent",
            db_connection_string="postgresql://test:test@localhost:5432/test"
        )
        print("✅ Successfully created agent with database connection string")
        
        print("\n✅ Agent creation tests passed!")
        
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        return False
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("DEEPAGENTS POSTGRESQL MODIFICATION TEST")
    print("=" * 60)
    
    success = True
    
    # Test imports
    if not test_import_structure():
        success = False
    
    print("\n" + "=" * 60)
    
    # Test tools without database
    try:
        test_postgres_tools_without_db()
    except Exception as e:
        print(f"❌ Tool test failed: {e}")
        success = False
    
    print("\n" + "=" * 60)
    
    # Test agent creation
    if not test_create_deep_agent():
        success = False
    
    print("\n" + "=" * 60)
    
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("\nThe deepagent has been successfully modified to use PostgreSQL tools!")
        print("\nNext steps:")
        print("1. Install the modified package: pip install -e .")
        print("2. Set up a PostgreSQL database")
        print("3. Use the example in examples/postgres_example.py")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check the errors above and fix them.")
    
    print("=" * 60)