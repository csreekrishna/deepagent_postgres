#!/usr/bin/env python3
"""
Test script to verify the read-only database agent works correctly and blocks modifications.
"""

import sys
import os

# Add the src directory to the path so we can import deepagents
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from deepagents.tools import postgres_query, postgres_schema, postgres_analyze
from deepagents.state import DeepAgentState


def test_readonly_security():
    """Test that modification queries are blocked."""
    print("Testing read-only security features...")
    
    # Create a mock state WITH a fake database connection to test query blocking
    state = DeepAgentState(messages=[], db_connection="fake_connection_for_testing")
    
    # Test dangerous queries that should be blocked
    dangerous_queries = [
        "INSERT INTO users (name) VALUES ('hacker')",
        "UPDATE users SET name = 'modified' WHERE id = 1", 
        "DELETE FROM users WHERE id = 1",
        "DROP TABLE users",
        "CREATE TABLE malicious (id INT)",
        "ALTER TABLE users ADD COLUMN hacked VARCHAR(100)",
        "TRUNCATE TABLE users",
        "GRANT ALL ON users TO public",
        "REVOKE SELECT ON users FROM user",
    ]
    
    for query in dangerous_queries:
        print(f"\n🔒 Testing blocked query: {query[:50]}...")
        result = postgres_query.invoke({"query": query, "state": state})
        if "Modification operations are not allowed" in result or "are strictly forbidden" in result:
            print("✅ Query correctly blocked")
        else:
            print(f"❌ Query was not blocked! Result: {result}")
            return False
    
    # Test allowed queries
    allowed_queries = [
        "SELECT * FROM users",
        "SELECT COUNT(*) FROM orders", 
        "WITH cte AS (SELECT * FROM users) SELECT * FROM cte",
        "EXPLAIN SELECT * FROM users",
    ]
    
    for query in allowed_queries:
        print(f"\n✅ Testing allowed query: {query[:50]}...")
        result = postgres_query.invoke({"query": query, "state": state})
        # Should get database connection error, not blocked query error
        if "No database connection available" in result:
            print("✅ Query allowed (database connection error expected)")
        elif "Modification operations are not allowed" in result:
            print(f"❌ Valid query was incorrectly blocked! Query: {query}")
            return False
        else:
            print(f"✅ Query processed correctly: {result[:100]}...")
    
    print("\n🎉 All security tests passed!")
    return True


def test_import_readonly_tools():
    """Test that all read-only tools can be imported."""
    print("Testing import of read-only tools...")
    
    try:
        from deepagents.graph import create_deep_agent
        print("✅ Successfully imported create_deep_agent")
        
        from deepagents.tools import write_todos, postgres_query, postgres_schema, postgres_analyze
        print("✅ Successfully imported all read-only postgres tools")
        
        # Try to import the old execute tool - should fail
        try:
            from deepagents.tools import postgres_execute
            print("❌ postgres_execute tool still exists! It should have been removed.")
            return False
        except ImportError:
            print("✅ postgres_execute tool correctly removed")
        
        from deepagents.state import DeepAgentState
        print("✅ Successfully imported DeepAgentState")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False


def test_create_readonly_agent():
    """Test creating a read-only deep agent."""
    print("Testing create_deep_agent with read-only PostgreSQL tools...")
    
    try:
        from deepagents.graph import create_deep_agent
        
        # Test creating agent with database connection string
        agent = create_deep_agent(
            tools=[],
            instructions="Test read-only database agent",
            db_connection_string="postgresql://test:test@localhost:5432/test"
        )
        print("✅ Successfully created read-only agent with database connection string")
        print(f"✅ Agent type: {type(agent)}")
        
        print("\n✅ Agent creation tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        return False


def test_tool_functionality():
    """Test the functionality of read-only tools."""
    print("Testing read-only tool functionality...")
    
    # Create a mock state without database connection
    state = DeepAgentState(messages=[])
    
    # Test postgres_query with valid SELECT
    print("\n1. Testing postgres_query with SELECT...")
    result = postgres_query.invoke({"query": "SELECT 1 as test", "state": state})
    print(f"Result: {result[:100]}...")
    
    # Test postgres_schema
    print("\n2. Testing postgres_schema...")
    result = postgres_schema.invoke({"state": state})
    print(f"Result: {result[:100]}...")
    
    # Test postgres_analyze
    print("\n3. Testing postgres_analyze...")
    result = postgres_analyze.invoke({"state": state})
    print(f"Result: {result[:100]}...")
    
    print("\n✅ All tool functionality tests completed!")
    return True


if __name__ == "__main__":
    print("=" * 70)
    print("DEEPAGENTS READ-ONLY DATABASE MODIFICATION TEST")
    print("=" * 70)
    
    success = True
    
    # Test imports
    if not test_import_readonly_tools():
        success = False
    
    print("\n" + "=" * 70)
    
    # Test security features
    if not test_readonly_security():
        success = False
    
    print("\n" + "=" * 70)
    
    # Test agent creation
    if not test_create_readonly_agent():
        success = False
    
    print("\n" + "=" * 70)
    
    # Test tool functionality
    if not test_tool_functionality():
        success = False
    
    print("\n" + "=" * 70)
    
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("\nThe deepagent has been successfully modified to be READ-ONLY!")
        print("\n✅ Security Features:")
        print("  - INSERT, UPDATE, DELETE operations are blocked")
        print("  - CREATE, DROP, ALTER operations are blocked") 
        print("  - TRUNCATE, GRANT, REVOKE operations are blocked")
        print("  - Only SELECT, WITH, and EXPLAIN queries are allowed")
        print("\n✅ Available Tools:")
        print("  - postgres_query: Execute SELECT queries (read-only)")
        print("  - postgres_schema: Get table schema information")
        print("  - postgres_analyze: Perform database analysis and statistics")
        print("  - write_todos: Plan and track analysis tasks")
        print("\nNext steps:")
        print("1. Install the modified package: pip install -e .")
        print("2. Set up a PostgreSQL database")
        print("3. Use the example in examples/postgres_example.py")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check the errors above and fix them.")
    
    print("=" * 70)