# 🧠🗄️ Deep Agents - PostgreSQL Edition

Using an LLM to call tools in a loop is the simplest form of an agent. 
This architecture, however, can yield agents that are "shallow" and fail to plan and act over longer, more complex tasks. 
Applications like "Deep Research", "Manus", and "Claude Code" have gotten around this limitation by implementing a combination of core components:
a **planning tool**, **sub agents**, access to **persistent storage**, a **detailed prompt**, and **comprehensive observability**.

> **🔥 This Version:** Specialized for **PostgreSQL database analysis** with **Phoenix tracing** - perfect for data analysts, researchers, and developers who need AI agents that can explore and analyze databases with full observability.

```mermaid
graph TB
    User[👤 User Input] --> Agent[🧠 DeepAgent LLM]
    
    Agent --> Planning[📋 Planning Tool<br/>write_todos]
    Agent --> SubAgent[🤖 Sub Agents<br/>Context Quarantine]
    Agent --> DBTools[🗄️ PostgreSQL Tools]
    Agent --> CustomTools[🔧 Custom Tools]
    
    DBTools --> Query[📊 postgres_query<br/>SELECT operations only]
    DBTools --> Schema[📋 postgres_schema<br/>Table structure info]
    DBTools --> Analyze[📈 postgres_analyze<br/>Statistics & insights]
    
    Query --> DB[(🗃️ PostgreSQL Database<br/>Read-Only Access)]
    Schema --> DB
    Analyze --> DB
    
    %% Phoenix Tracing Layer
    Agent -.-> Phoenix[🔭 Phoenix Tracing]
    Planning -.-> Phoenix
    SubAgent -.-> Phoenix
    DBTools -.-> Phoenix
    CustomTools -.-> Phoenix
    
    Phoenix --> Dashboard[📊 Phoenix Dashboard<br/>localhost:6006]
    Phoenix --> Traces[📈 LLM Calls<br/>Tool Executions<br/>DB Operations<br/>Performance Metrics]
    
    %% Styling
    classDef llm fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    classDef tools fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef db fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef tracing fill:#fff3e0,stroke:#e65100,stroke-width:2px,stroke-dasharray: 5 5
    
    class Agent llm
    class Planning,SubAgent,DBTools,CustomTools,Query,Schema,Analyze tools
    class DB db
    class Phoenix,Dashboard,Traces tracing
```

**Current Architecture Features:**
- **🧠 LLM-Powered Agent** with detailed system prompts
- **📋 Planning Tool** for task breakdown and tracking  
- **🤖 Sub Agents** for context quarantine and specialized tasks
- **🗄️ PostgreSQL Tools** for read-only database operations
- **🔭 Phoenix Tracing** for comprehensive observability

This **PostgreSQL Edition** of `deepagents` implements these components specifically for database analysis workflows. Unlike the original file system version, this edition provides:

- **🗄️ Read-only PostgreSQL tools** for safe database exploration
- **🔭 Phoenix tracing** for complete LLM and database operation observability  
- **🔒 Security-first approach** preventing any database modifications
- **📊 Advanced analytics** with table statistics and schema analysis

**Acknowledgements: This project was primarily inspired by Claude Code, and initially was largely an attempt to see what made Claude Code general purpose, and make it even more so.**

## Installation

> **⚠️ Important:** This is a specialized PostgreSQL + Phoenix tracing version of DeepAgents. The original `pip install deepagents` installs a different version with file system tools.

### Install This PostgreSQL Version

```bash
# Clone this specific repository
git clone https://github.com/csreekrishna/deepagent_postgres.git
cd deepagent_postgres

# Install in development mode
pip install -e .
```

### Prerequisites

- **Python 3.11+**
- **PostgreSQL database** (local or remote)
- **OpenAI API key** or **Anthropic API key**

```bash
# Set your API key (choose one)
export OPENAI_API_KEY="your-openai-key"
# OR
export ANTHROPIC_API_KEY="your-anthropic-key"
```

### Quick Setup with Docker PostgreSQL

```bash
# Start PostgreSQL with sample data (included in this repo)
docker run -d \
  --name deepagent-postgres \
  -e POSTGRES_DB=deepagent_test \
  -e POSTGRES_USER=deepagent \
  -e POSTGRES_PASSWORD=test123 \
  -p 5432:5432 \
  postgres:15

# Load sample e-commerce data
docker cp sample_data.sql deepagent-postgres:/tmp/
docker exec deepagent-postgres psql -U deepagent -d deepagent_test -f /tmp/sample_data.sql

# Test the connection
python test_phoenix_tracing.py
```

The test will start Phoenix dashboard at `http://localhost:6006` for observability.

## Usage

### Basic PostgreSQL Agent Example

```python
import os
from deepagents import create_deep_agent

# Database connection string - modify to match your PostgreSQL setup
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
    db_connection_string="postgresql://deepagent:test123@localhost:5432/deepagent_test"
)

# Invoke the agent
result = agent.invoke({"messages": [{"role": "user", "content": "Research LangGraph and analyze any related data in the database"}]})
```

See `test_phoenix_tracing.py` in this repository for a complete working example with Phoenix tracing.

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

By default, `deepagents` will use OpenAI GPT-4o if `OPENAI_API_KEY` is set, otherwise Claude Sonnet 4. You can pass any [LangChain model object](https://python.langchain.com/docs/integrations/chat/) to use a different model.

**Built-in Model Functions:**
```python
from deepagents import get_openai_model, get_anthropic_model

# Use specific OpenAI model
agent = create_deep_agent(
    tools=[],
    instructions="Your instructions...",
    model=get_openai_model(model_name="gpt-4o", temperature=0.1)
)

# Use specific Anthropic model  
agent = create_deep_agent(
    tools=[],
    instructions="Your instructions...",
    model=get_anthropic_model(model_name="claude-3-5-sonnet-20241022")
)
```

**Custom LangChain Models:**
```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# Custom OpenAI model
custom_openai = ChatOpenAI(model="gpt-4o-mini", temperature=0.5)

# Custom Anthropic model
custom_anthropic = ChatAnthropic(model="claude-3-haiku-20240307")

# Google Gemini model
custom_gemini = ChatGoogleGenerativeAI(model="gemini-pro")

agent = create_deep_agent(
    tools=[],
    instructions="Your instructions...",
    model=custom_openai  # or custom_anthropic, custom_gemini, etc.
)
```

### `db_connection_string` (Optional)

A PostgreSQL connection string to enable database tools. When provided, the agent will have access to `postgres_query`, `postgres_schema`, and `postgres_analyze` tools.

Format: `"postgresql://username:password@host:port/database_name"`

**Examples:**
```python
# Basic database connection
agent = create_deep_agent(
    tools=[],
    instructions="Database assistant instructions...",
    db_connection_string="postgresql://deepagent:test123@localhost:5432/deepagent_test"
)

# With custom model and database
from deepagents import get_openai_model

agent = create_deep_agent(
    tools=[],
    instructions="Advanced database analyst...",
    model=get_openai_model(model_name="gpt-4o", temperature=0),
    db_connection_string="postgresql://deepagent:test123@localhost:5432/deepagent_test"
)
```

## Deep Agent Details

The below components are built into `deepagents` and helps make it work for deep tasks off-the-shelf.

### System Prompt

`deepagents` comes with a [built-in system prompt](src/deepagents/prompts.py). This is relatively detailed prompt that is heavily based on and inspired by [attempts](https://github.com/kn1026/cc/blob/main/claudecode.md) to [replicate](https://github.com/asgeirtj/system_prompts_leaks/blob/main/Anthropic/claude-code.md)
Claude Code's system prompt. It was made more general purpose than Claude Code's system prompt.
This contains detailed instructions for how to use the built-in planning tool, PostgreSQL database tools, and sub agents.
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

## Phoenix Tracing Integration

DeepAgent now includes **Phoenix by Arize AI** tracing for comprehensive observability of LLM calls, tool executions, and PostgreSQL operations.

### Automatic Tracing Setup

Phoenix tracing is enabled by default when creating a DeepAgent:

```python
from deepagents import create_deep_agent

# Tracing is automatically enabled
agent = create_deep_agent(
    tools=[],
    instructions="Your database analyst instructions...",
    db_connection_string="postgresql://user:password@localhost:5432/db",
    enable_tracing=True,  # Default: True
    tracing_project_name="my-project"  # Default: "deepagent-postgres"
)
```

### Manual Phoenix Server Control

```python
from deepagents import start_phoenix_server, get_phoenix_url, PhoenixTracer

# Start Phoenix server manually
start_phoenix_server(port=6006)
print(f"Phoenix dashboard: {get_phoenix_url()}")

# Or use context manager for automatic cleanup
with PhoenixTracer(project_name="my-analysis") as tracer:
    agent = create_deep_agent(tools=[], instructions="...")
    result = agent.invoke({"messages": [{"role": "user", "content": "Analyze database"}]})
```

### What Gets Traced

Phoenix automatically traces:
- **LLM calls** (OpenAI GPT-4o, Anthropic Claude)
- **Tool executions** (postgres_query, postgres_schema, postgres_analyze, write_todos)
- **Database operations** with query details and performance metrics
- **Agent workflows** and sub-agent spawning
- **Error handling** and exception details

### Viewing Traces

1. Phoenix dashboard runs at `http://localhost:6006` by default
2. View real-time traces, spans, and performance metrics
3. Analyze LLM token usage and costs
4. Debug tool execution flows and database queries
5. Monitor agent performance and identify bottlenecks

### Dependencies

Phoenix tracing requires these additional dependencies (auto-installed):
- `arize-phoenix[evals]>=4.0.0`
- `openinference-instrumentation-langchain>=0.1.0`

### Disabling Tracing

```python
# Disable tracing for performance-critical applications
agent = create_deep_agent(
    tools=[],
    instructions="...",
    enable_tracing=False
)
```

## Roadmap
- [ ] Allow users to customize full system prompt
- [ ] Code cleanliness (type hinting, docstrings, formating)
- [ ] Add more advanced PostgreSQL analysis capabilities
- [ ] Create an example of a deep coding agent built on top of this
- [ ] Benchmark PostgreSQL analysis performance with different database sizes
- [ ] Add human-in-the-loop support for tools
