#!/bin/bash

# Simple DeepAgent PostgreSQL Chat Interface Startup
set -e

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

echo "🚀 Starting DeepAgent PostgreSQL Chat..."

# Check if .env exists
if [ ! -f .env ]; then
    print_warning "No .env file found. Please add your API keys to .env"
    print_info "Creating template .env file..."
    cat > .env << EOF
# API Keys - Add your key here
OPENAI_API_KEY=your-openai-key-here
# ANTHROPIC_API_KEY=your-anthropic-key-here

# Database Configuration  
DATABASE_URL=postgresql://deepagent:test123@localhost:5432/deepagent_test

# Tracing
ENABLE_TRACING=true
TRACING_PROJECT_NAME=deepagent-chat
EOF
    print_warning "Please edit .env with your API keys and run this script again"
    exit 1
fi

# Check for API keys
if grep -q "your-openai-key-here\|your-anthropic-key-here" .env; then
    print_warning "Please update .env file with your actual API keys"
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    print_info "Shutting down..."
    jobs -p | xargs -r kill
    print_success "Stopped"
    exit 0
}
trap cleanup SIGINT SIGTERM

print_info "Starting DeepAgent LangGraph server..."

# Start the LangGraph server with our DeepAgent
npx --yes @langchain/langgraph-cli@latest dev \
    --port 2024 \
    --host 0.0.0.0 \
    --config langgraph.json &

BACKEND_PID=$!
print_success "DeepAgent server started (PID: $BACKEND_PID)"

# Wait a moment for backend to start
sleep 3

print_info "Starting Chat UI..."

# Start the chat UI
cd deepagent-chat-ui
npm run dev &
FRONTEND_PID=$!
cd ..

print_success "Chat UI started (PID: $FRONTEND_PID)"

echo ""
print_success "🎉 DeepAgent PostgreSQL Chat is running!"
echo ""
print_info "💬 Chat Interface: http://localhost:3000"
print_info "🔧 DeepAgent API: http://localhost:2024"
print_info "📊 Phoenix Tracing: http://localhost:6006"
echo ""
print_info "Configuration:"
print_info "  • Assistant ID: deepagent_postgres"
print_info "  • Database: $(grep DATABASE_URL .env | cut -d'=' -f2)"
echo ""
print_warning "Press Ctrl+C to stop both servers"

# Wait for all background jobs
wait