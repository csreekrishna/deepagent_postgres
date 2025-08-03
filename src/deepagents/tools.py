from langchain_core.tools import tool, InjectedToolCallId
from langgraph.types import Command
from langchain_core.messages import ToolMessage
from typing import Annotated, Any
from langgraph.prebuilt import InjectedState
import psycopg2
import asyncpg
import asyncio
from contextlib import asynccontextmanager

from deepagents.prompts import (
    WRITE_TODOS_DESCRIPTION,
    POSTGRES_QUERY_DESCRIPTION,
    POSTGRES_SCHEMA_DESCRIPTION,
    POSTGRES_ANALYZE_DESCRIPTION,
)
from deepagents.state import Todo, DeepAgentState


@tool(description=WRITE_TODOS_DESCRIPTION)
def write_todos(
    todos: list[Todo], tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    return Command(
        update={
            "todos": todos,
            "messages": [
                ToolMessage(f"Updated todo list to {todos}", tool_call_id=tool_call_id)
            ],
        }
    )


@tool(description=POSTGRES_QUERY_DESCRIPTION)
def postgres_query(
    query: str,
    state: Annotated[DeepAgentState, InjectedState],
    limit: int = 1000,
) -> str:
    """Execute a SELECT query against the PostgreSQL database. Only read operations are allowed."""
    try:
        db_connection = state.get("db_connection")
        if not db_connection:
            return "Error: No database connection available. Database connection should be established at startup."
        
        # Security check: Only allow SELECT statements and read-only operations
        query_upper = query.upper().strip()
        forbidden_keywords = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 'TRUNCATE', 'GRANT', 'REVOKE']
        
        if any(keyword in query_upper for keyword in forbidden_keywords):
            return f"Error: Modification operations are not allowed. Only SELECT queries are permitted. Forbidden operation detected in query."
        
        if not query_upper.startswith('SELECT') and not query_upper.startswith('WITH') and not query_upper.startswith('EXPLAIN'):
            return "Error: Only SELECT, WITH (CTE), and EXPLAIN queries are allowed."
        
        conn = psycopg2.connect(db_connection)
        cursor = conn.cursor()
        
        # Add LIMIT to SELECT queries if not present and limit is reasonable
        if query_upper.startswith('SELECT') and 'LIMIT' not in query_upper and limit > 0:
            query = f"{query} LIMIT {limit}"
        
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description] if cursor.description else []
        
        cursor.close()
        conn.close()
        
        if not results:
            return "Query executed successfully. No rows returned."
        
        # Format results as a table with better formatting
        result_lines = []
        if column_names:
            # Create header
            header = "\t".join(column_names)
            result_lines.append(header)
            result_lines.append("-" * len(header))
        
        # Add data rows
        for row in results:
            formatted_row = []
            for val in row:
                if val is None:
                    formatted_row.append("NULL")
                elif isinstance(val, (int, float)):
                    formatted_row.append(str(val))
                else:
                    # Truncate long strings for readability
                    str_val = str(val)
                    if len(str_val) > 100:
                        str_val = str_val[:97] + "..."
                    formatted_row.append(str_val)
            result_lines.append("\t".join(formatted_row))
        
        # Add summary info
        result_lines.append("")
        result_lines.append(f"Total rows returned: {len(results)}")
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error executing query: {str(e)}"




@tool(description=POSTGRES_SCHEMA_DESCRIPTION)
def postgres_schema(
    state: Annotated[DeepAgentState, InjectedState],
    table_name: str = None,
) -> str:
    """Get schema information for PostgreSQL database tables."""
    try:
        db_connection = state.get("db_connection")
        if not db_connection:
            return "Error: No database connection available. Database connection should be established at startup."
        
        conn = psycopg2.connect(db_connection)
        cursor = conn.cursor()
        
        if table_name:
            # Get schema for specific table
            cursor.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = %s 
                ORDER BY ordinal_position
            """, (table_name,))
            results = cursor.fetchall()
            
            if not results:
                cursor.close()
                conn.close()
                return f"Table '{table_name}' not found."
            
            result_lines = [f"Schema for table '{table_name}':"]
            result_lines.append("Column Name\tData Type\tNullable\tDefault")
            result_lines.append("-" * 60)
            
            for row in results:
                result_lines.append(f"{row[0]}\t{row[1]}\t{row[2]}\t{row[3] or 'None'}")
        else:
            # Get list of all tables
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """)
            results = cursor.fetchall()
            
            if not results:
                cursor.close()
                conn.close()
                return "No tables found in the database."
            
            result_lines = ["Available tables:"]
            for row in results:
                result_lines.append(f"- {row[0]}")
        
        cursor.close()
        conn.close()
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error getting schema: {str(e)}"


@tool(description=POSTGRES_ANALYZE_DESCRIPTION)
def postgres_analyze(
    state: Annotated[DeepAgentState, InjectedState],
    table_name: str = None,
    analysis_type: str = "basic",
) -> str:
    """Perform analysis on PostgreSQL database tables to get insights like row counts, data distribution, etc."""
    try:
        db_connection = state.get("db_connection")
        if not db_connection:
            return "Error: No database connection available. Database connection should be established at startup."
        
        conn = psycopg2.connect(db_connection)
        cursor = conn.cursor()
        
        if table_name:
            # Analyze specific table
            if analysis_type == "basic":
                # Get basic table statistics
                cursor.execute(f"""
                    SELECT 
                        schemaname,
                        tablename,
                        attname as column_name,
                        n_distinct,
                        correlation
                    FROM pg_stats 
                    WHERE tablename = %s
                    ORDER BY attname
                """, (table_name,))
                stats_results = cursor.fetchall()
                
                # Get row count
                cursor.execute(f"""
                    SELECT COUNT(*) as total_rows 
                    FROM {table_name}
                """)
                row_count = cursor.fetchone()[0]
                
                # Get table size
                cursor.execute(f"""
                    SELECT pg_size_pretty(pg_total_relation_size(%s)) as table_size
                """, (table_name,))
                table_size = cursor.fetchone()[0]
                
                result_lines = [f"Analysis for table '{table_name}':"]
                result_lines.append("=" * 50)
                result_lines.append(f"Total rows: {row_count:,}")
                result_lines.append(f"Table size: {table_size}")
                result_lines.append("")
                result_lines.append("Column Statistics:")
                result_lines.append("Column\t\tDistinct Values\tCorrelation")
                result_lines.append("-" * 50)
                
                for row in stats_results:
                    schema, table, col_name, n_distinct, correlation = row
                    n_distinct_str = str(n_distinct) if n_distinct else "N/A"
                    correlation_str = f"{correlation:.3f}" if correlation else "N/A"
                    result_lines.append(f"{col_name}\t\t{n_distinct_str}\t\t{correlation_str}")
            
            elif analysis_type == "detailed":
                # Get detailed column analysis
                cursor.execute(f"""
                    SELECT column_name, data_type, is_nullable, column_default
                    FROM information_schema.columns 
                    WHERE table_name = %s 
                    ORDER BY ordinal_position
                """, (table_name,))
                columns = cursor.fetchall()
                
                result_lines = [f"Detailed Analysis for table '{table_name}':"]
                result_lines.append("=" * 60)
                
                for col_name, data_type, is_nullable, default_val in columns:
                    result_lines.append(f"\nColumn: {col_name}")
                    result_lines.append(f"  Type: {data_type}")
                    result_lines.append(f"  Nullable: {is_nullable}")
                    result_lines.append(f"  Default: {default_val or 'None'}")
                    
                    # Get sample values for the column
                    try:
                        cursor.execute(f"""
                            SELECT DISTINCT {col_name} 
                            FROM {table_name} 
                            WHERE {col_name} IS NOT NULL 
                            LIMIT 5
                        """)
                        samples = [str(row[0]) for row in cursor.fetchall()]
                        if samples:
                            result_lines.append(f"  Sample values: {', '.join(samples)}")
                    except:
                        pass  # Skip if there are issues with the column
        else:
            # Analyze all tables
            cursor.execute("""
                SELECT 
                    schemaname,
                    tablename,
                    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
                FROM pg_tables 
                WHERE schemaname = 'public'
                ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
            """)
            table_results = cursor.fetchall()
            
            result_lines = ["Database Overview:"]
            result_lines.append("=" * 50)
            result_lines.append("Schema\t\tTable\t\tSize")
            result_lines.append("-" * 50)
            
            for schema, table, size in table_results:
                result_lines.append(f"{schema}\t\t{table}\t\t{size}")
                
            # Get total database size
            cursor.execute("SELECT pg_size_pretty(pg_database_size(current_database()))")
            db_size = cursor.fetchone()[0]
            result_lines.append("")
            result_lines.append(f"Total database size: {db_size}")
        
        cursor.close()
        conn.close()
        
        return "\n".join(result_lines)
        
    except Exception as e:
        return f"Error performing analysis: {str(e)}"
