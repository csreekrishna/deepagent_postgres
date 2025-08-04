import { RunnableConfig } from "@langchain/core/runnables";
import { MessagesAnnotation, StateGraph } from "@langchain/langgraph";
import { spawn } from "child_process";
import { promisify } from "util";
import path from "path";

import { ConfigurationSchema, ensureConfiguration } from "./configuration.js";

const execAsync = promisify(spawn);

// Define the function that calls our Python DeepAgent
async function callDeepAgent(
  state: typeof MessagesAnnotation.State,
  config: RunnableConfig,
): Promise<typeof MessagesAnnotation.Update> {
  const configuration = ensureConfiguration(config);
  
  // Get the last user message
  const messages = state.messages;
  const lastMessage = messages[messages.length - 1];
  const userQuery = lastMessage.content as string;

  try {
    // Call our Python DeepAgent via subprocess
    const pythonScript = path.join(process.cwd(), '../../../chat_interface.py');
    
    const result = await new Promise<string>((resolve, reject) => {
      const process = spawn('python', [pythonScript], {
        stdio: ['pipe', 'pipe', 'pipe'],
        env: {
          ...process.env,
          DATABASE_URL: configuration.databaseUrl,
          ENABLE_TRACING: configuration.enableTracing.toString(),
          TRACING_PROJECT_NAME: configuration.tracingProjectName,
          USER_QUERY: userQuery
        }
      });

      let stdout = '';
      let stderr = '';

      process.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      process.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      process.on('close', (code) => {
        if (code === 0) {
          resolve(stdout.trim());
        } else {
          reject(new Error(`Python process failed with code ${code}: ${stderr}`));
        }
      });

      // Send the user query to the Python process
      process.stdin.write(JSON.stringify({ query: userQuery, config: configuration }));
      process.stdin.end();
    });

    return { 
      messages: [{ 
        role: "assistant", 
        content: result || "I apologize, but I couldn't process your request. Please try again." 
      }] 
    };

  } catch (error) {
    console.error("DeepAgent error:", error);
    return { 
      messages: [{ 
        role: "assistant", 
        content: `I encountered an error while processing your request: ${error.message}. Please check that the PostgreSQL database is running and accessible.` 
      }] 
    };
  }
}

// Create the graph
const workflow = new StateGraph(MessagesAnnotation)
  .addNode("agent", callDeepAgent)
  .addEdge("__start__", "agent")
  .addEdge("agent", "__end__");

export const graph = workflow.compile({
  checkpointer: false, // We can add checkpointing later if needed
});

graph.name = "DeepAgent PostgreSQL Analyst";