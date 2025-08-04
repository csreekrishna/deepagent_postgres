#!/bin/bash

# DeepAgent PostgreSQL Chat UI Setup Script
# This script sets up the official LangChain Agent Chat UI for DeepAgent

set -e

echo "🧠 Setting up DeepAgent PostgreSQL Chat UI..."

# Configuration
UI_DIR="deepagent-chat-ui"
BACKEND_PORT=2024
UI_PORT=3000
ASSISTANT_ID="deepagent_postgres"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_step() {
    echo -e "${BLUE}▶ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 20+ first."
    exit 1
fi

# Check if Python environment is set up
if ! python -c "import deepagents" &> /dev/null; then
    print_warning "DeepAgents package not found. Make sure you've installed it with: pip install -e ."
fi

# Step 1: Create the chat UI if it doesn't exist
if [ ! -d "$UI_DIR" ]; then
    print_step "Creating LangChain Agent Chat UI..."
    npx create-agent-chat-app@latest \
        --project-name "$UI_DIR" \
        --package-manager npm \
        --yes
    print_success "Chat UI created in $UI_DIR"
else
    print_success "Chat UI directory already exists: $UI_DIR"
fi

# Step 2: Configure environment variables
print_step "Configuring environment variables..."

cd "$UI_DIR"

# Create .env.local file with DeepAgent configuration
cat > .env.local << EOF
# DeepAgent PostgreSQL Configuration
NEXT_PUBLIC_API_URL=http://localhost:$BACKEND_PORT
NEXT_PUBLIC_ASSISTANT_ID=$ASSISTANT_ID

# Optional: LangSmith tracing (leave empty for local development)
# NEXT_PUBLIC_LANGSMITH_API_KEY=your-langsmith-key

# Backend configuration will be handled by the LangGraph server
EOF

print_success "Environment configured (.env.local created)"

# Step 3: Create backend configuration
print_step "Setting up backend configuration..."

cd ..

# Create langgraph.json for the backend
cat > langgraph.json << EOF
{
  "dependencies": ["."],
  "graphs": {
    "$ASSISTANT_ID": "./deepagent_graph.py:graph"
  },
  "env": ".env"
}
EOF

# Create the graph file for DeepAgent
cat > deepagent_graph.py << EOF
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
EOF

# Create .env file for backend (both locations)
if [ ! -f .env ]; then
    cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql://deepagent:test123@localhost:5432/deepagent_test

# API Keys (add your keys here)
OPENAI_API_KEY=your-openai-key-here
# ANTHROPIC_API_KEY=your-anthropic-key-here

# Phoenix Tracing
ENABLE_TRACING=true
TRACING_PROJECT_NAME=deepagent-chat-ui

# Optional: Tavily for web search (not required for DeepAgent PostgreSQL)
# TAVILY_API_KEY=your-tavily-key
EOF
    print_success "Backend environment template created (.env)"
    print_warning "Please edit .env file with your API keys"
else
    print_success "Backend .env file already exists"
fi

# Copy .env to chat UI directory for LangGraph CLI
if [ -f .env ]; then
    cp .env "$UI_DIR/.env"
    print_success ".env copied to chat UI directory"
fi

print_success "Backend configuration complete"

# Step 4: Create launch script
print_step "Creating launch script..."

cat > start-deepagent-chat.sh << 'EOF'
#!/bin/bash

# Start DeepAgent PostgreSQL Chat Interface
set -e

UI_DIR="deepagent-chat-ui"
BACKEND_PORT=2024
UI_PORT=3000

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

echo "🚀 Starting DeepAgent PostgreSQL Chat Interface..."

# Check if .env exists
if [ ! -f .env ]; then
    print_warning "No .env file found. Please run setup-chat-ui.sh first."
    exit 1
fi

# Check for API keys
if grep -q "your-openai-key-here\|your-anthropic-key-here" .env; then
    print_warning "Please update .env file with your actual API keys"
fi

# Function to start backend
start_backend() {
    print_info "Starting LangGraph API server on port $BACKEND_PORT..."
    npx --yes @langchain/langgraph-cli@latest dev \
        --port $BACKEND_PORT \
        --host 0.0.0.0 \
        --config langgraph.json &
    BACKEND_PID=$!
    echo $BACKEND_PID > .backend.pid
    print_success "Backend server started (PID: $BACKEND_PID)"
}

# Function to start frontend  
start_frontend() {
    print_info "Starting Chat UI on port $UI_PORT..."
    cd "$UI_DIR"
    npm run dev -- --port $UI_PORT &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../.frontend.pid
    cd ..
    print_success "Frontend started (PID: $FRONTEND_PID)"
}

# Cleanup function
cleanup() {
    echo ""
    print_info "Shutting down servers..."
    
    if [ -f .backend.pid ]; then
        BACKEND_PID=$(cat .backend.pid)
        kill $BACKEND_PID 2>/dev/null || true
        rm .backend.pid
        print_success "Backend server stopped"
    fi
    
    if [ -f .frontend.pid ]; then
        FRONTEND_PID=$(cat .frontend.pid)
        kill $FRONTEND_PID 2>/dev/null || true
        rm .frontend.pid
        print_success "Frontend stopped"
    fi
    
    print_success "DeepAgent Chat Interface stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start services
start_backend
sleep 3  # Wait for backend to start

start_frontend
sleep 2  # Wait for frontend to start

echo ""
print_success "🎉 DeepAgent PostgreSQL Chat Interface is running!"
echo ""
print_info "💬 Chat Interface: http://localhost:$UI_PORT"
print_info "🔧 API Server: http://localhost:$BACKEND_PORT"
print_info "📊 Phoenix Tracing: http://localhost:6006 (if enabled)"
echo ""
print_info "Configuration:"
print_info "  • Assistant ID: deepagent_postgres"
print_info "  • Database: Check your .env file for DATABASE_URL"
print_info "  • Tracing: Enabled (check ENABLE_TRACING in .env)"
echo ""
print_warning "Press Ctrl+C to stop both servers"

# Wait for processes
wait
EOF

chmod +x start-deepagent-chat.sh

print_success "Launch script created (start-deepagent-chat.sh)"

# Final instructions
echo ""
print_success "🎉 DeepAgent PostgreSQL Chat UI setup complete!"
echo ""
print_info "Next steps:"
echo "1. Edit .env file with your API keys (OpenAI or Anthropic)"
echo "2. Ensure PostgreSQL is running with your database"
echo "3. Run: ./start-deepagent-chat.sh"
echo ""
print_info "The setup includes:"
echo "• Official LangChain Agent Chat UI in '$UI_DIR/'"
echo "• DeepAgent PostgreSQL backend configuration"
echo "• Environment configuration for seamless connection"
echo "• Launch script to start both frontend and backend"
echo ""
print_warning "Remember to configure your database connection in .env"