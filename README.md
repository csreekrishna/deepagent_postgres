# 🧠🤖Deep Agents

Using an LLM to call tools in a loop is the simplest form of an agent. 
This architecture, however, can yield agents that are "shallow" and fail to plan and act over longer, more complex tasks. 
Applications like "Deep Research", "Manus", and "Claude Code" have gotten around this limitation by implementing a combination of four things:
a **planning tool**, **sub agents**, access to **persistent storage**, and a **detailed prompt**.

<img src="deep_agents.png" alt="deep agent" width="600"/>

`deepagents` is a Python package that implements these in a general purpose way so that you can easily create a Deep Agent for your application. This version has been modified to use **PostgreSQL database tools** instead of file system tools for more robust data persistence and querying capabilities.

**Acknowledgements: This project was primarily inspired by Claude Code, and initially was largely an attempt to see what made Claude Code general purpose, and make it even more so.**

## Installation

```bash
pip install deepagents
```

## Usage

### Basic PostgreSQL Agent Example

```python
import os
from deepagents import create_deep_agent

# Database connection string - modify to match your PostgreSQL setup
db_connection_string = os.getenv(
    "DATABASE_URL", 
    "postgresql://username:password@localhost:5432/your_database"
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

# Create the agent with PostgreSQL tools
agent = create_deep_agent(
    tools=[],  # No additional tools needed for basic database operations
    instructions=instructions,
    db_connection_string=db_connection_string
)

# Invoke the agent
result = agent.invoke({"messages": [{"role": "user", "content": "Show me all tables and their schemas"}]})
```

### Research Agent with Database Storage

(To run the example below, will need to `pip install tavily-python`)

```python
import os
from typing import Literal

from tavily import TavilyClient
from deepagents import create_deep_agent


# Search tool to use to do research
def internet_search(
    query: str,
    max_results: int = 5,
    topic: Literal["general", "news", "finance"] = "general",
    include_raw_content: bool = False,
):
    """Run a web search"""
    tavily_async_client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    return tavily_async_client.search(
        query,
        max_results=max_results,
        include_raw_content=include_raw_content,
        topic=topic,
    )


# Prompt prefix to steer the agent to be an expert researcher
research_instructions = """You are an expert researcher. Your job is to conduct thorough research, and then write a polished report.

You have access to internet search tools and can store research findings in the database.

## `internet_search`

Use this to run an internet search for a given query. You can specify the number of results, the topic, and whether raw content should be included.

## Database Tools

You can analyze research data stored in the PostgreSQL database using read-only database tools.
"""

# Create the agent with both search and database capabilities
agent = create_deep_agent(
    [internet_search],
    research_instructions,
    db_connection_string="postgresql://user:password@localhost:5432/research_db"
)

# Invoke the agent
result = agent.invoke({"messages": [{"role": "user", "content": "Research LangGraph and analyze any related data in the database"}]})
```

See [examples/research/research_agent.py](examples/research/research_agent.py) for a more complex example.

The agent created with `create_deep_agent` is just a LangGraph graph - so you can interact with it (streaming, human-in-the-loop, memory, studio)
in the same way you would any LangGraph agent.

## Creating a custom deep agent

There are several parameters you can pass to `create_deep_agent` to create your own custom deep agent.

### `tools` (Required)

The first argument to `create_deep_agent` is `tools`.
This should be a list of functions or LangChain `@tool` objects.
The agent (and any subagents) will have access to these tools.

### `instructions` (Required)

The second argument to `create_deep_agent` is `instructions`.
This will serve as part of the prompt of the deep agent.
Note that there is a [built in system prompt](#built-in-prompt) as well, so this is not the *entire* prompt the agent will see.

### `subagents` (Optional)

A keyword-only argument to `create_deep_agent` is `subagents`.
This can be used to specify any custom subagents this deep agent will have access to.
You can read more about why you would want to use subagents [here](#sub-agents)

`subagents` should be a list of dictionaries, where each dictionary follow this schema:

```python
class SubAgent(TypedDict):
    name: str
    description: str
    prompt: str
    tools: NotRequired[list[str]]
```

- **name**: This is the name of the subagent, and how the main agent will call the subagent
- **description**: This is the description of the subagent that is shown to the main agent
- **prompt**: This is the prompt used for the subagent
- **tools**: This is the list of tools that the subagent has access to. By default will have access to all tools passed in, as well as all built-in tools.

To use it looks like:

```python
research_sub_agent = {
    "name": "research-agent",
    "description": "Used to research more in depth questions",
    "prompt": sub_research_prompt,
}
subagents = [research_subagent]
agent = create_deep_agent(
    tools,
    prompt,
    subagents=subagents
)
```

### `model` (Optional)

By default, `deepagents` will use `"claude-sonnet-4-20250514"`. If you want to use a different model,
you can pass a [LangChain model object](https://python.langchain.com/docs/integrations/chat/).

### `db_connection_string` (Optional)

A PostgreSQL connection string to enable database tools. When provided, the agent will have access to `postgres_query`, `postgres_execute`, and `postgres_schema` tools.

Format: `"postgresql://username:password@host:port/database_name"`

Example:
```python
agent = create_deep_agent(
    tools=[],
    instructions="Database assistant instructions...",
    db_connection_string="postgresql://user:password@localhost:5432/mydb"
)
```

## Deep Agent Details

The below components are built into `deepagents` and helps make it work for deep tasks off-the-shelf.

### System Prompt

`deepagents` comes with a [built-in system prompt](src/deepagents/prompts.py). This is relatively detailed prompt that is heavily based on and inspired by [attempts](https://github.com/kn1026/cc/blob/main/claudecode.md) to [replicate](https://github.com/asgeirtj/system_prompts_leaks/blob/main/Anthropic/claude-code.md)
Claude Code's system prompt. It was made more general purpose than Claude Code's system prompt.
This contains detailed instructions for how to use the built-in planning tool, file system tools, and sub agents.
Note that part of this system prompt [can be customized](#promptprefix--required-)

Without this default system prompt - the agent would not be nearly as successful at going as it is.
The importance of prompting for creating a "deep" agent cannot be understated.

### Planing Tool

`deepagents` comes with a built-in planning tool. This planning tool is very simple and is based on ClaudeCode's TodoWrite tool.
This tool doesn't actually do anything - it is just a way for the agent to come up with a plan, and then have that in the context to help keep it on track.

### PostgreSQL Database Tools (Read-Only)

`deepagents` comes with three built-in PostgreSQL database tools for read-only operations: `postgres_query`, `postgres_schema`, `postgres_analyze`.
These tools connect to a real PostgreSQL database for robust data analysis and exploration capabilities.

- **`postgres_query`**: Execute SELECT queries to retrieve data from the database (read-only, no modifications allowed)
- **`postgres_schema`**: Get schema information about database tables and columns  
- **`postgres_analyze`**: Perform analysis on tables to get insights, statistics, row counts, and data distribution

The database connection is established at startup by passing a `db_connection_string` parameter to `create_deep_agent`.

**Security**: All database operations are strictly read-only. Any attempt to modify the database (INSERT, UPDATE, DELETE, CREATE, DROP, etc.) will be blocked and result in an error.

```python
# Database connection string format
db_connection_string = "postgresql://username:password@host:port/database_name"

agent = create_deep_agent(
    tools=[],
    instructions="...",
    db_connection_string=db_connection_string
)

# The agent will automatically have access to all PostgreSQL tools
result = agent.invoke({
    "messages": [{"role": "user", "content": "Show me all tables in the database"}]
})
```

**Requirements**: You need to have PostgreSQL installed and running, with the database credentials accessible to the agent.

### Sub Agents

`deepagents` comes with the built-in ability to call sub agents (based on Claude Code).
It has access to a `general-purpose` subagent at all times - this is a subagent with the same instructions as the main agent and all the tools that is has access to.
You can also specify [custom sub agents](#subagents--optional-) with their own instructions and tools.

Sub agents are useful for ["context quarantine"](https://www.dbreunig.com/2025/06/26/how-to-fix-your-context.html#context-quarantine) (to help not pollute the overall context of the main agent)
as well as custom instructions.

## Roadmap
- [ ] Allow users to customize full system prompt
- [ ] Code cleanliness (type hinting, docstrings, formating)
- [ ] Allow for more of a robust virtual filesystem
- [ ] Create an example of a deep coding agent built on top of this
- [ ] Benchmark the example of [deep research agent](examples/research/research_agent.py)
- [ ] Add human-in-the-loop support for tools
