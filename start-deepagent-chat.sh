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
    npm run dev &
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
