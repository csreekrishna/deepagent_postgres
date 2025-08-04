# DeepAgent PostgreSQL Chat UI

A modern chat interface for interacting with DeepAgent PostgreSQL + Phoenix tracing through the official LangChain Agent Chat UI.

## Features

- 💬 **Modern Chat Interface** - Clean, responsive chat UI built with Next.js
- 🗄️ **PostgreSQL Integration** - Connect to any PostgreSQL database with read-only security
- 🔭 **Phoenix Tracing** - Full observability of LLM calls, tool executions, and database operations
- 📊 **Real-time Monitoring** - View traces and performance metrics through Phoenix dashboard
- 🧠 **Deep Agent Capabilities** - Advanced planning, sub-agents, and complex analysis workflows

## Quick Start

### Prerequisites

- Node.js 20+
- Python 3.11+
- PostgreSQL database (local or remote)
- OpenAI API key or Anthropic API key

### 1. Install Dependencies

```bash
# From the project root
cd agent-chat-app
npm install
```

### 2. Configure Environment

```bash
# Copy and edit the environment file
cp .env.example .env
```

Edit `.env` with your API keys:
```bash
# Choose one (OpenAI recommended)
OPENAI_API_KEY=your-openai-key-here
ANTHROPIC_API_KEY=your-anthropic-key-here

# PostgreSQL Database
DATABASE_URL=postgresql://deepagent:test123@localhost:5432/deepagent_test

# Phoenix Tracing
ENABLE_TRACING=true
TRACING_PROJECT_NAME=deepagent-chat-ui
```

### 3. Set Up PostgreSQL Database

**Option A: Use Docker (Recommended)**
```bash
# Start PostgreSQL with sample e-commerce data
docker run -d \
  --name deepagent-postgres \
  -e POSTGRES_DB=deepagent_test \
  -e POSTGRES_USER=deepagent \
  -e POSTGRES_PASSWORD=test123 \
  -p 5432:5432 \
  postgres:15

# Load sample data
docker cp ../sample_data.sql deepagent-postgres:/tmp/
docker exec deepagent-postgres psql -U deepagent -d deepagent_test -f /tmp/sample_data.sql
```

**Option B: Connect to Existing Database**
Update `DATABASE_URL` in `.env` with your database credentials.

### 4. Start Development Servers

```bash
npm run dev
```

This starts:
- **Web UI**: http://localhost:3000 (or http://localhost:3001 if port 3000 is in use)
- **LangGraph API**: http://localhost:2024

### 5. Access Chat Interface

1. Open http://localhost:3000 in your browser (or the port shown in your terminal if 3000 is occupied)
2. Configure the chat interface:
   - **Deployment URL**: `http://localhost:2024`
   - **Assistant ID**: `deepagent_postgres`
   - **LangSmith API Key**: Leave empty for local development

3. Start chatting with your database!

## Example Queries

Try these sample queries to explore your database:

```
Show me all tables in the database

Get the schema for the users table

Find the top 5 customers by order value

Analyze product sales trends from the orders table

What are the most reviewed products?

Show me order statistics by month
```

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Next.js UI    │    │  LangGraph API  │    │  Python Bridge  │
│  (localhost:3000) │────│ (localhost:2024) │────│ chat_interface.py │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                                                       ▼
                                            ┌─────────────────┐
                                            │   DeepAgent     │
                                            │   PostgreSQL    │
                                            │   + Phoenix     │
                                            └─────────────────┘
```

## Observability

### Phoenix Tracing Dashboard

When Phoenix tracing is enabled, you can monitor:

- **LLM Calls**: Token usage, costs, response times
- **Database Operations**: Query performance, results, errors  
- **Tool Executions**: Success rates, execution times
- **Agent Workflows**: Planning, sub-agent spawning, task completion

Access the Phoenix dashboard at: http://localhost:6006

### Monitoring Features

- Real-time trace visualization
- Performance metrics and bottleneck identification
- Cost tracking for LLM usage
- Error analysis and debugging
- Query optimization insights

## Production Deployment

For production deployment:

1. **Database Security**: Use read-only database users
2. **API Key Management**: Use secure environment variable storage
3. **Phoenix Tracing**: Configure production tracing endpoint
4. **Authentication**: Add user authentication to the chat interface
5. **Rate Limiting**: Implement rate limiting for API calls

## Troubleshooting

### Common Issues

**Database Connection Failed**
- Verify PostgreSQL is running
- Check DATABASE_URL credentials
- Ensure network connectivity

**Phoenix Tracing Errors**
- Phoenix server errors are normal if Phoenix isn't running
- Set `ENABLE_TRACING=false` to disable tracing
- Tracing failures don't affect core functionality

**Python Import Errors**
- Ensure Python virtual environment is activated
- Verify deepagents package is installed: `pip install -e ..`

### Debug Mode

Enable debug logging:
```bash
export DEBUG=1
npm run dev
```

## Development

### Adding Custom Tools

1. Add new tool functions to the Python DeepAgent
2. Update the instructions in `configuration.ts`
3. Test through the chat interface

### Customizing the Interface

The chat UI is built with:
- **Next.js 15** - React framework
- **Tailwind CSS** - Styling
- **LangGraph** - Agent orchestration
- **shadcn/ui** - UI components

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with sample database
5. Submit a pull request

## License

This project inherits the MIT license from the original DeepAgent implementation.