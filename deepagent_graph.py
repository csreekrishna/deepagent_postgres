"""
DeepAgent PostgreSQL Graph for LangGraph API Server
"""
import os
from typing import Annotated, Dict, Any
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode
from langchain_core.runnables import RunnableConfig
from typing_extensions import TypedDict

# Import DeepAgent
try:
    from deepagents import create_deep_agent
except ImportError:
    print("DeepAgents not installed. Please run: pip install -e .")
    raise

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def create_deepagent_node():
    \"\"\"Create the DeepAgent PostgreSQL node\"\"\"
    
    # Get database connection from environment
    db_connection_string = os.getenv(
        "DATABASE_URL", 
        "postgresql://deepagent:test123@localhost:5432/deepagent_test"
    )
    
    # Instructions for the database agent
    instructions = \"\"\"You are a database analyst that helps users explore and analyze their PostgreSQL database.

You can:
- Query data from tables using postgres_query (SELECT statements only)  
- Explore database schema using postgres_schema
- Analyze tables and get insights using postgres_analyze
- Plan and track complex analysis tasks using write_todos

Always use postgres_schema first to understand the database structure before writing queries.
All operations are read-only - you cannot modify the database in any way.
\"\"\"
    
    # Create the DeepAgent
    agent = create_deep_agent(
        tools=[],  # Built-in PostgreSQL tools will be added automatically
        instructions=instructions,
        db_connection_string=db_connection_string,
        enable_tracing=True,
        tracing_project_name="deepagent-chat-ui"
    )
    
    return agent

# Create the agent
deepagent = create_deepagent_node()

def call_deepagent(state: State, config: RunnableConfig) -> Dict[str, Any]:
    \"\"\"Call the DeepAgent with the current state\"\"\"
    response = deepagent.invoke(state, config)
    return {"messages": response["messages"]}

# Build the graph
workflow = StateGraph(State)
workflow.add_node("agent", call_deepagent)
workflow.set_entry_point("agent")
workflow.set_finish_point("agent")

graph = workflow.compile()
