# 🧠🗄️💬 Deep Agents - PostgreSQL Edition with Chat UI

Using an LLM to call tools in a loop is the simplest form of an agent. 
This architecture, however, can yield agents that are "shallow" and fail to plan and act over longer, more complex tasks. 
Applications like "Deep Research", "Manus", and "Claude Code" have gotten around this limitation by implementing a combination of core components:
a **planning tool**, **sub agents**, access to **persistent storage**, a **detailed prompt**, and **comprehensive observability**.

> **🔥 This Version:** Complete **PostgreSQL database analysis** platform with **modern chat interface** and **Phoenix tracing** - perfect for data analysts, researchers, and developers who need conversational AI agents for database exploration with enterprise-grade observability.

## 🚀 Two Ways to Use DeepAgent

### 💬 Chat Interface (Recommended)
- **Modern chat UI** at http://localhost:3000 (or http://localhost:3001 if port 3000 is in use)
- **Natural language** database queries and analysis
- **Real-time** conversation with your PostgreSQL database
- **Visual interface** for complex data exploration workflows

### 🐍 Python API (Advanced)
- **Programmatic access** for custom applications
- **Direct integration** into existing Python workflows
- **Full control** over agent configuration and execution

```mermaid
graph TB
    %% Chat Interface Path
    User[👤 User] --> ChatUI[💬 Chat Interface<br/>localhost:3000]
    ChatUI --> LangGraphAPI[🔗 LangGraph API<br/>localhost:2024]
    LangGraphAPI --> PythonBridge[🐍 Python Bridge<br/>chat_interface.py]
    
    %% Direct Python Path
    User -.-> PythonAPI[🐍 Python API<br/>Direct Integration]
    PythonAPI -.-> Agent
    
    %% Core DeepAgent Architecture
    PythonBridge --> Agent[🧠 DeepAgent LLM]
    
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
    
    %% Response Flow
    Agent --> PythonBridge
    PythonBridge --> LangGraphAPI
    LangGraphAPI --> ChatUI
    ChatUI --> User
    
    %% Styling
    classDef ui fill:#e8f5e8,stroke:#2e7d32,stroke-width:3px
    classDef api fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
    classDef llm fill:#e1f5fe,stroke:#01579b,stroke-width:3px
    classDef tools fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef db fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef tracing fill:#fff3e0,stroke:#e65100,stroke-width:2px,stroke-dasharray: 5 5
    
    class ChatUI,User ui
    class LangGraphAPI,PythonBridge,PythonAPI api
    class Agent llm
    class Planning,SubAgent,DBTools,CustomTools,Query,Schema,Analyze tools
    class DB db
    class Phoenix,Dashboard,Traces tracing
```

## ✨ Key Features

### 💬 Modern Chat Interface
- **Conversational Database Analysis** - Ask questions in natural language
- **Real-time Responses** - Instant feedback and interactive exploration
- **Visual Chat History** - Track your analysis journey
- **Mobile-Friendly** - Responsive design for any device

### 🧠 Advanced AI Capabilities  
- **LLM-Powered Agent** with detailed system prompts (OpenAI GPT-4o or Anthropic Claude)
- **Planning Tool** for complex multi-step analysis workflows
- **Sub Agents** for context quarantine and specialized tasks
- **Memory Management** for conversation continuity

### 🗄️ PostgreSQL Integration
- **Read-Only Security** - Safe database exploration without modification risks
- **Schema Discovery** - Automatic table and column exploration
- **Query Optimization** - Intelligent query generation and execution
- **Data Analysis** - Advanced statistics and insights generation

### 🔭 Enterprise Observability
- **Phoenix Tracing** - Complete visibility into LLM calls, database operations, and agent workflows
- **Performance Monitoring** - Query execution times and bottleneck identification  
- **Cost Tracking** - LLM token usage and expense monitoring
- **Error Analysis** - Detailed debugging and troubleshooting

### 🔒 Security & Reliability
- **Read-Only Database Access** - Prevents accidental data modifications
- **SQL Injection Protection** - Secure query validation and sanitization
- **Error Handling** - Graceful failure recovery and user feedback
- **Audit Trail** - Complete logging of all database interactions

**Acknowledgements: This project was primarily inspired by Claude Code, and initially was largely an attempt to see what made Claude Code general purpose, and make it even more so.**

## 🚀 Quick Start

> **⚠️ Important:** This is a specialized PostgreSQL + Phoenix tracing version of DeepAgents. The original `pip install deepagents` installs a different version with file system tools.

### Option 1: Chat Interface (Recommended for Most Users)

**Perfect for:** Data analysts, researchers, business users who want to chat with their database

```bash
# 1. Clone the repository
git clone https://github.com/csreekrishna/deepagent_postgres.git
cd deepagent_postgres

# 2. Set up Python environment
pip install -e .

# 3. Set up Chat Interface (uses official LangChain Agent Chat UI)
./setup-chat-ui.sh

# 4. Configure your API keys
# Edit .env file with your OpenAI or Anthropic API key

# 5. Start both frontend and backend
./start-deepagent-chat.sh
```

Access the chat interface at **http://localhost:3000**

### Option 2: Python API (Advanced Users)

**Perfect for:** Developers integrating into existing applications, custom workflows

```bash
# 1. Clone and install
git clone https://github.com/csreekrishna/deepagent_postgres.git
cd deepagent_postgres
pip install -e .

# 2. Set API keys
export OPENAI_API_KEY="your-openai-key"  # OR
export ANTHROPIC_API_KEY="your-anthropic-key"

# 3. Test with sample script
python test_phoenix_tracing.py
```

### Prerequisites

- **Python 3.11+**
- **Node.js 20+** (for chat interface)
- **PostgreSQL database** (local or remote)
- **OpenAI API key** or **Anthropic API key**

### 🗄️ Database Setup (Both Options)

**Quick Setup with Docker (Recommended):**

```bash
# Start PostgreSQL with sample e-commerce data
docker run -d \
  --name deepagent-postgres \
  -e POSTGRES_DB=deepagent_test \
  -e POSTGRES_USER=deepagent \
  -e POSTGRES_PASSWORD=test123 \
  -p 5432:5432 \
  postgres:15

# Load sample data (8 tables with realistic e-commerce data)
docker cp sample_data.sql deepagent-postgres:/tmp/
docker exec deepagent-postgres psql -U deepagent -d deepagent_test -f /tmp/sample_data.sql
```

**Or connect to your existing PostgreSQL database** by updating the connection string.

## 💬 Usage Examples

### Chat Interface Usage

Once you've started the chat interface (`./start-deepagent-chat.sh`), visit **http://localhost:3000** and configure:

1. **Deployment URL**: `http://localhost:2024`
2. **Assistant ID**: `deepagent_postgres` 
3. **LangSmith API Key**: Leave empty for local development

The setup script automatically configures these values, but you can change them if needed.

**Sample Chat Conversations:**

```
👤 You: Show me all tables in the database

🤖 DeepAgent: I found 8 tables in your e-commerce database:
• users - Customer information
• products - Product catalog 
• categories - Product categories
• orders - Customer orders
• order_items - Individual order line items  
• reviews - Product reviews
• order_summary - Aggregated order data (view)
• product_stats - Product statistics (view)

Would you like me to explore any specific table?

👤 You: Find the top 5 customers by total order value

🤖 DeepAgent: Here are your top 5 customers by total order value:

1. Emily Brown (emily.brown@email.com) - $742.89
2. David Wilson (david.w@email.com) - $653.21  
3. Jane Smith (jane.smith@email.com) - $524.33
4. Mike Johnson (mike.j@email.com) - $487.76
5. John Doe (john.doe@email.com) - $398.45

These 5 customers represent 45% of your total revenue. Would you like me to analyze their purchasing patterns?
```

### Python API Usage

**Basic PostgreSQL Agent Example**

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

## 🔭 Phoenix Observability Dashboard

Both the **Chat Interface** and **Python API** include comprehensive Phoenix tracing for complete observability.

### What You Can Monitor

**🎯 Real-time Dashboard** at `http://localhost:6006`:
- **LLM Conversations** - Every chat message, token usage, response times
- **Database Queries** - SQL execution, performance metrics, result sizes
- **Agent Planning** - Todo creation, sub-agent spawning, workflow progression
- **Error Analysis** - Failed queries, debugging information, recovery actions
- **Cost Tracking** - Token usage, API costs, optimization opportunities

### Automatic Tracing Setup

**Chat Interface**: Tracing is configured in the `.env` file:
```bash
ENABLE_TRACING=true
TRACING_PROJECT_NAME=deepagent-chat-ui
```

**Python API**: Tracing is enabled by default:
```python
agent = create_deep_agent(
    tools=[],
    instructions="Your instructions...",
    db_connection_string="postgresql://...",
    enable_tracing=True,  # Default: True
    tracing_project_name="my-analysis"
)
```

### Production Monitoring

For production deployments:
- **Performance Optimization** - Identify slow queries and bottlenecks
- **Cost Management** - Track LLM usage and implement budgets
- **Quality Assurance** - Monitor conversation quality and user satisfaction
- **Security Auditing** - Review all database access and query patterns

## 🔧 Troubleshooting

### Chat Interface Issues

**"Cannot connect to LangGraph server"**
```bash
# Check if servers are running
npm run dev  # Should start both web and API servers

# Verify endpoints
curl http://localhost:3000  # Web interface
curl http://localhost:2024  # LangGraph API
```

**"DeepAgent not found"**
- Ensure Python virtual environment is activated
- Verify deepagents package is installed: `pip install -e .`
- Check Python path in `chat_interface.py`

### Database Connection Issues

**"Database connection failed"**
```bash
# Test PostgreSQL connection
docker ps  # Check if container is running
psql -h localhost -U deepagent -d deepagent_test  # Test direct connection

# Check credentials in .env file
DATABASE_URL=postgresql://deepagent:test123@localhost:5432/deepagent_test
```

**"No tables found"**
```bash
# Reload sample data
docker exec deepagent-postgres psql -U deepagent -d deepagent_test -f /tmp/sample_data.sql
```

### Phoenix Tracing Issues

**"Phoenix server not accessible"**
- Phoenix tracing errors don't affect core functionality
- Set `ENABLE_TRACING=false` to disable if needed
- Phoenix dashboard requires separate server start for advanced features

### Performance Issues

**"Slow query responses"**
- Check database query complexity in Phoenix dashboard
- Consider adding database indexes for frequently queried columns
- Monitor LLM response times for optimization opportunities

**"High token usage"**
- Review conversation history in Phoenix dashboard  
- Use more specific queries to reduce context
- Consider switching to more cost-effective models

## 🚀 Production Deployment

### Chat Interface Production

**Docker Deployment:**
```bash
# Build production image
cd deepagent-chat-ui
docker build -t deepagent-chat .

# Run with environment variables
docker run -d \
  --name deepagent-chat \
  -p 3000:3000 \
  -p 2024:2024 \
  -e OPENAI_API_KEY=your-key \
  -e DATABASE_URL=your-production-db \
  deepagent-chat
```

**Security Considerations:**
- Use read-only database users in production
- Implement authentication and authorization
- Set up rate limiting for API endpoints
- Use HTTPS with proper SSL certificates
- Monitor and audit all database access

**Scaling Options:**
- Deploy web interface on CDN/edge servers
- Run LangGraph API on container orchestration (Kubernetes)
- Use managed PostgreSQL services (AWS RDS, Google Cloud SQL)
- Implement caching layers for frequently accessed data

### Python API Production

**Package Installation:**
```python
# Install as package dependency
pip install git+https://github.com/csreekrishna/deepagent_postgres.git

# Use in production applications
from deepagents import create_deep_agent
agent = create_deep_agent(
    tools=[],
    instructions="Production database analyst",
    db_connection_string=os.getenv("DATABASE_URL"),
    enable_tracing=True
)
```

## 🛣️ Roadmap

### Current Features ✅
- [x] PostgreSQL read-only database tools
- [x] Phoenix tracing and observability  
- [x] Modern chat interface with LangGraph integration
- [x] Planning tools and sub-agent support
- [x] OpenAI and Anthropic model support
- [x] Docker deployment configuration
- [x] Comprehensive documentation and examples

### Coming Soon 🚧
- [ ] **Authentication & Authorization** - User management and access control
- [ ] **Multi-Database Support** - MySQL, SQLite, BigQuery connectors
- [ ] **Advanced Visualizations** - Charts, graphs, and data visualization components
- [ ] **Conversation Export** - Save and share analysis sessions
- [ ] **Custom Tool Integration** - Plugin system for domain-specific tools
- [ ] **Automated Insights** - ML-powered pattern detection and recommendations

### Future Enhancements 🔮
- [ ] **Natural Language Queries** - Even more sophisticated query understanding
- [ ] **Collaborative Features** - Multi-user sessions and team workspaces
- [ ] **Scheduled Analysis** - Automated reports and monitoring
- [ ] **Integration APIs** - Webhooks and third-party service connections
- [ ] **Advanced Security** - Row-level security and data masking
- [ ] **Performance Optimization** - Query caching and connection pooling

## 🤝 Contributing

We welcome contributions! Here's how to get started:

1. **Fork the repository** on GitHub
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Run the test suite**: `python -m pytest`
5. **Update documentation** as needed
6. **Submit a pull request** with a clear description

### Development Setup
```bash
# Clone and set up development environment
git clone https://github.com/csreekrishna/deepagent_postgres.git
cd deepagent_postgres
pip install -e ".[dev]"

# Set up chat interface for development  
./setup-chat-ui.sh
# Edit .env with your API keys
./start-deepagent-chat.sh
```

### Areas We Need Help With
- 🧪 **Testing** - Unit tests, integration tests, performance benchmarks
- 📚 **Documentation** - Tutorials, examples, API documentation
- 🎨 **UI/UX** - Chat interface improvements and new visualizations
- 🔧 **Integrations** - New database connectors and tool integrations
- 🐛 **Bug Fixes** - Issue resolution and stability improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **LangChain Team** - For the amazing LangChain and LangGraph frameworks
- **Arize AI** - For Phoenix observability and tracing capabilities
- **Claude Code** - Original inspiration for the Deep Agent architecture
- **PostgreSQL Community** - For the robust database system
- **Open Source Contributors** - For making this project possible
