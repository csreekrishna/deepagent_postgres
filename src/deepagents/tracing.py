"""Phoenix tracing setup for DeepAgent.

This module handles the initialization and configuration of Phoenix AI observability
for tracing LLM calls, tool executions, and database operations.
"""

import os
import logging
from typing import Optional
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor

logger = logging.getLogger(__name__)


def setup_phoenix_tracing(
    project_name: str = "deepagent-postgres",
    endpoint: Optional[str] = None,
    auto_instrument: bool = True
) -> bool:
    """
    Set up Phoenix tracing for DeepAgent.
    
    Args:
        project_name: Name of the project in Phoenix dashboard
        endpoint: Phoenix collector endpoint (defaults to local Phoenix server)
        auto_instrument: Whether to auto-instrument LangChain/LangGraph
        
    Returns:
        bool: True if setup was successful, False otherwise
    """
    try:
        # Set up Phoenix collector endpoint if provided (for local Phoenix, use default)
        if endpoint:
            os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = endpoint
        else:
            # For local Phoenix server, use local OTLP endpoint
            os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "http://localhost:4317"
            
        # Register Phoenix tracer
        tracer_provider = register(
            project_name=project_name,
            auto_instrument=auto_instrument
        )
        
        # Explicitly instrument LangChain for comprehensive tracing
        if not auto_instrument:
            LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
            
        logger.info(f"Phoenix tracing initialized for project: {project_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize Phoenix tracing: {e}")
        return False


def start_phoenix_server(port: int = 6006) -> bool:
    """
    Start a local Phoenix server.
    
    Args:
        port: Port to run Phoenix server on
        
    Returns:
        bool: True if server started successfully, False otherwise
    """
    try:
        import phoenix as px
        
        # Start Phoenix server
        session = px.launch_app(port=port)
        logger.info(f"Phoenix server started at http://localhost:{port}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to start Phoenix server: {e}")
        return False


def get_phoenix_url(port: int = 6006) -> str:
    """Get the Phoenix dashboard URL."""
    return f"http://localhost:{port}"


class PhoenixTracer:
    """Context manager for Phoenix tracing."""
    
    def __init__(self, project_name: str = "deepagent-postgres", start_server: bool = True, port: int = 6006):
        self.project_name = project_name
        self.start_server = start_server
        self.port = port
        self.server_started = False
        
    def __enter__(self):
        """Enter the tracing context."""
        if self.start_server:
            self.server_started = start_phoenix_server(self.port)
            
        setup_phoenix_tracing(self.project_name)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the tracing context."""
        if self.server_started:
            logger.info("Phoenix tracing context ended")