from deepagents.sub_agent import _create_task_tool, SubAgent
from deepagents.model import get_default_model, get_openai_model, get_anthropic_model
from deepagents.tools import write_todos, postgres_query, postgres_schema, postgres_analyze
from deepagents.state import DeepAgentState
from deepagents.tracing import setup_phoenix_tracing
from typing import Sequence, Union, Callable, Any, TypeVar, Type, Optional
from langchain_core.tools import BaseTool
from langchain_core.language_models import LanguageModelLike

from langgraph.prebuilt import create_react_agent

StateSchema = TypeVar("StateSchema", bound=DeepAgentState)
StateSchemaType = Type[StateSchema]

base_prompt = """You have access to a number of standard tools

## `write_todos`

You have access to the `write_todos` tools to help you manage and plan tasks. Use these tools VERY frequently to ensure that you are tracking your tasks and giving the user visibility into your progress.
These tools are also EXTREMELY helpful for planning tasks, and for breaking down larger complex tasks into smaller steps. If you do not use this tool when planning, you may forget to do important tasks - and that is unacceptable.

It is critical that you mark todos as completed as soon as you are done with a task. Do not batch up multiple tasks before marking them as completed.

## Database Tools (Read-Only)

You have access to PostgreSQL database tools for READ-ONLY operations:
- `postgres_query`: Execute SELECT queries to retrieve data from the database (read-only, no modifications allowed)
- `postgres_schema`: Get schema information about database tables and columns
- `postgres_analyze`: Perform analysis on tables to get insights, statistics, row counts, and data distribution

The database connection is established at startup. These tools provide comprehensive read-only access to explore and analyze the PostgreSQL database.

IMPORTANT: You can only READ from the database. All modification operations (INSERT, UPDATE, DELETE, CREATE, DROP, etc.) are strictly forbidden and will result in errors.

## `task`

- When doing web search, prefer to use the `task` tool in order to reduce context usage."""


def create_deep_agent(
    tools: Sequence[Union[BaseTool, Callable, dict[str, Any]]],
    instructions: str,
    model: Optional[Union[str, LanguageModelLike]] = None,
    subagents: list[SubAgent] = None,
    state_schema: Optional[StateSchemaType] = None,
    db_connection_string: Optional[str] = None,
    enable_tracing: bool = True,
    tracing_project_name: str = "deepagent-postgres",
):
    """Create a deep agent.

    This agent will by default have access to a tool to write todos (write_todos),
    and three PostgreSQL read-only database tools: postgres_query, postgres_schema, postgres_analyze.

    Args:
        tools: The additional tools the agent should have access to.
        instructions: The additional instructions the agent should have. Will go in
            the system prompt.
        model: The model to use.
        subagents: The subagents to use. Each subagent should be a dictionary with the
            following keys:
                - `name`
                - `description` (used by the main agent to decide whether to call the sub agent)
                - `prompt` (used as the system prompt in the subagent)
                - (optional) `tools`
        state_schema: The schema of the deep agent. Should subclass from DeepAgentState
        db_connection_string: PostgreSQL connection string (e.g., "postgresql://user:password@localhost:5432/dbname")
        enable_tracing: Whether to enable Phoenix tracing (default: True)
        tracing_project_name: Name for the Phoenix tracing project (default: "deepagent-postgres")
    """
    # Initialize Phoenix tracing if enabled
    if enable_tracing:
        setup_phoenix_tracing(tracing_project_name)
    
    prompt = instructions + base_prompt
    built_in_tools = [write_todos, postgres_query, postgres_schema, postgres_analyze]
    if model is None:
        model = get_default_model()
    state_schema = state_schema or DeepAgentState
    task_tool = _create_task_tool(
        list(tools) + built_in_tools,
        instructions,
        subagents or [],
        model,
        state_schema
    )
    all_tools = built_in_tools + list(tools) + [task_tool]
    
    # Create initial state with database connection
    initial_state = {}
    if db_connection_string:
        initial_state["db_connection"] = db_connection_string
    
    agent = create_react_agent(
        model,
        prompt=prompt,
        tools=all_tools,
        state_schema=state_schema,
    )
    
    # If we have a database connection, we need to modify the agent to include it in initial state
    if db_connection_string:
        original_invoke = agent.invoke
        
        def invoke_with_db(input_data, config=None, **kwargs):
            if isinstance(input_data, dict):
                input_data = {**input_data, "db_connection": db_connection_string}
            else:
                # Handle string inputs by converting to dict
                input_data = {"messages": [{"role": "user", "content": input_data}], "db_connection": db_connection_string}
            return original_invoke(input_data, config, **kwargs)
        
        agent.invoke = invoke_with_db
    
    return agent
