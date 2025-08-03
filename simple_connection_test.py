#!/usr/bin/env python3
"""
Simple connection test for PostgreSQL database and OpenAI API.
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


def test_postgres_connection():
    """Test PostgreSQL connection."""
    print("🔍 Testing PostgreSQL connection...")
    
    try:
        import psycopg2
        
        # Database connection string
        db_connection_string = "postgresql://deepagent:test123@localhost:5432/deepagent_test"
        
        conn = psycopg2.connect(db_connection_string)
        cursor = conn.cursor()
        
        # Test basic queries
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"✅ PostgreSQL connected: {version}")
        
        # Check our data
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM products") 
        product_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM orders")
        order_count = cursor.fetchone()[0]
        
        print(f"✅ Database has {user_count} users, {product_count} products, {order_count} orders")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False


def test_openai_connection():
    """Test OpenAI API connection."""
    print("\n🔍 Testing OpenAI API connection...")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("Please set it with: export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    try:
        from deepagents import get_openai_model
        
        # Create OpenAI model
        model = get_openai_model(model_name="gpt-4o", temperature=0)
        print("✅ OpenAI model created successfully")
        
        # Test a simple query
        response = model.invoke("Hello! Respond with just 'OpenAI connection successful'")
        print(f"✅ OpenAI API response: {response.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI connection failed: {e}")
        return False


def test_deepagent_tools():
    """Test DeepAgent tools with database."""
    print("\n🔍 Testing DeepAgent tools...")
    
    try:
        from deepagents.tools import postgres_query, postgres_schema
        from deepagents.state import DeepAgentState
        
        # Create state with database connection
        state = DeepAgentState(
            messages=[],
            db_connection="postgresql://deepagent:test123@localhost:5432/deepagent_test"
        )
        
        # Test schema tool
        print("Testing postgres_schema tool...")
        schema_result = postgres_schema.invoke({"state": state})
        print(f"✅ Schema tool works: {schema_result[:100]}...")
        
        # Test query tool  
        print("Testing postgres_query tool...")
        query_result = postgres_query.invoke({
            "query": "SELECT COUNT(*) as total_users FROM users",
            "state": state
        })
        print(f"✅ Query tool works: {query_result}")
        
        return True
        
    except Exception as e:
        print(f"❌ DeepAgent tools failed: {e}")
        return False


def main():
    """Run all connection tests."""
    print("🚀 DeepAgent Connection Tests")
    print("=" * 40)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: PostgreSQL
    if test_postgres_connection():
        tests_passed += 1
    
    # Test 2: OpenAI
    if test_openai_connection():
        tests_passed += 1
    
    # Test 3: DeepAgent Tools
    if test_deepagent_tools():
        tests_passed += 1
    
    print(f"\n📊 Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All connection tests passed! Ready to run full DeepAgent test.")
        print("\nNext step: Run 'python test_with_openai_and_postgres.py'")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        return False


if __name__ == "__main__":
    main()