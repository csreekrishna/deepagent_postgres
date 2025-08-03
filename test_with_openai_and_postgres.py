#!/usr/bin/env python3
"""
Comprehensive test of DeepAgent with OpenAI model and real PostgreSQL database.
This script tests the full functionality with real data.
"""

import os
import sys
from datetime import datetime

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from deepagents import create_deep_agent, get_openai_model


def test_database_connection():
    """Test basic database connectivity."""
    print("🔍 Testing database connection...")
    
    # Database connection string
    db_connection_string = "postgresql://deepagent:test123@localhost:5432/deepagent_test"
    
    try:
        import psycopg2
        conn = psycopg2.connect(db_connection_string)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        
        print(f"✅ Database connected successfully! Found {user_count} users.")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def create_test_agent():
    """Create a DeepAgent with OpenAI model and database connection."""
    print("🤖 Creating DeepAgent with OpenAI model...")
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("Please set it with: export OPENAI_API_KEY='your-api-key-here'")
        return None

    # Database connection string
    db_connection_string = "postgresql://deepagent:test123@localhost:5432/deepagent_test"
    
    # Instructions for the agent
    instructions = """You are a senior data analyst specializing in e-commerce analytics. 
    
    You have access to a comprehensive e-commerce database with the following tables:
    - users: Customer information and demographics
    - categories: Product categories
    - products: Product catalog with pricing and inventory
    - orders: Customer orders and transaction data
    - order_items: Individual items within orders
    - reviews: Customer product reviews and ratings
    
    You can also access these views:
    - order_summary: Aggregated order information with customer details
    - product_stats: Product performance metrics including sales and ratings
    
    Your role is to:
    1. Explore and analyze the database structure
    2. Generate insights about customer behavior, sales trends, and product performance
    3. Answer business questions with data-driven analysis
    4. Provide recommendations based on the data
    
    Always start by understanding the database schema before performing analysis.
    All operations are read-only - you cannot modify the database.
    """
    
    try:
        # Create agent with OpenAI model explicitly
        agent = create_deep_agent(
            tools=[],
            instructions=instructions,
            model=get_openai_model(model_name="gpt-4o", temperature=0),
            db_connection_string=db_connection_string
        )
        
        print("✅ DeepAgent created successfully with OpenAI GPT-4o model!")
        return agent
        
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        return None


def run_test_scenarios(agent):
    """Run comprehensive test scenarios with the agent."""
    print("\n🧪 Running test scenarios...")
    
    test_scenarios = [
        {
            "name": "Database Schema Exploration",
            "query": "Show me all the tables in the database and give me an overview of the database structure."
        },
        {
            "name": "Basic Analytics",
            "query": "Analyze the users table and tell me about our customer demographics. How many users do we have from each country?"
        },
        {
            "name": "Sales Analysis", 
            "query": "Analyze our sales data. What are the top-selling products and what's our total revenue?"
        },
        {
            "name": "Product Performance",
            "query": "Which products have the highest ratings and most reviews? Show me the top 5 products by customer satisfaction."
        },
        {
            "name": "Order Status Analysis",
            "query": "Analyze our order statuses. How many orders are in each status and what's the distribution?"
        },
        {
            "name": "Category Performance",
            "query": "Which product categories are performing best in terms of sales volume and revenue?"
        },
        {
            "name": "Customer Insights",
            "query": "Tell me about our customer purchase behavior. Who are our top customers by order value?"
        }
    ]
    
    results = []
    
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {scenario['name']}")
        print(f"{'='*60}")
        print(f"Query: {scenario['query']}")
        print("\nAgent Response:")
        print("-" * 40)
        
        try:
            # Invoke the agent
            response = agent.invoke({
                "messages": [{"role": "user", "content": scenario['query']}]
            })
            
            # Extract the response content
            if 'messages' in response and response['messages']:
                last_message = response['messages'][-1]
                if hasattr(last_message, 'content'):
                    result = last_message.content
                else:
                    result = str(last_message)
            else:
                result = str(response)
            
            print(result)
            results.append({
                "scenario": scenario['name'],
                "query": scenario['query'],
                "success": True,
                "response": result[:500] + "..." if len(result) > 500 else result
            })
            
        except Exception as e:
            error_msg = f"❌ Error: {e}"
            print(error_msg)
            results.append({
                "scenario": scenario['name'],
                "query": scenario['query'],
                "success": False,
                "error": str(e)
            })
    
    return results


def print_summary(results):
    """Print test summary."""
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"Successful: {successful}")
    print(f"Failed: {total - successful}")
    print(f"Success Rate: {successful/total*100:.1f}%")
    
    if successful == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("DeepAgent is working perfectly with OpenAI and PostgreSQL!")
    else:
        print(f"\n⚠️  {total - successful} tests failed. Check the errors above.")
    
    print("\n📊 Database Information:")
    print("- Database: PostgreSQL 15")
    print("- Host: localhost:5432") 
    print("- Database: deepagent_test")
    print("- Tables: 6 (users, categories, products, orders, order_items, reviews)")
    print("- Views: 2 (order_summary, product_stats)")
    print("- Sample Data: E-commerce dataset with realistic transactions")
    
    print("\n🤖 AI Model Information:")
    print("- Model: OpenAI GPT-4o")
    print("- Framework: LangChain + LangGraph")
    print("- Capabilities: Read-only database analysis")


def main():
    """Main test function."""
    print("🚀 DeepAgent + OpenAI + PostgreSQL Integration Test")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Test database connection
    if not test_database_connection():
        print("\n❌ Database connection failed. Please ensure PostgreSQL is running.")
        print("Run: docker ps to check if deepagent-postgres container is running")
        return False
    
    # Step 2: Create agent
    agent = create_test_agent()
    if not agent:
        print("\n❌ Agent creation failed. Check OpenAI API key and dependencies.")
        return False
    
    # Step 3: Run test scenarios
    results = run_test_scenarios(agent)
    
    # Step 4: Print summary
    print_summary(results)
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    return True


if __name__ == "__main__":
    main()