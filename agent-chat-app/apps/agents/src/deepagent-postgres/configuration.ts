import { z } from "zod";

export const ConfigurationSchema = z.object({
  model: z.enum(["openai_gpt_4o", "anthropic_claude_3_5_sonnet"]).default("openai_gpt_4o"),
  systemPromptTemplate: z.string().default(
    `You are a PostgreSQL database analyst powered by DeepAgent. You help users explore and analyze their PostgreSQL database using read-only operations.

Current time: {system_time}

Available capabilities:
- Query data from tables using postgres_query (SELECT statements only)
- Explore database schema using postgres_schema  
- Analyze tables and get insights using postgres_analyze
- Plan and track complex analysis tasks using write_todos

Key features:
- All operations are READ-ONLY for security
- Phoenix tracing enabled for full observability
- Advanced planning and sub-agent capabilities
- Deep analysis workflows for complex database insights

Always start by exploring the database schema before writing queries. Be thorough in your analysis and provide actionable insights.`
  ),
  databaseUrl: z.string().default("postgresql://deepagent:test123@localhost:5432/deepagent_test"),
  enableTracing: z.boolean().default(true),
  tracingProjectName: z.string().default("deepagent-chat-ui")
});

export type Configuration = z.infer<typeof ConfigurationSchema>;

export function ensureConfiguration(
  config: Record<string, any>
): Configuration {
  return ConfigurationSchema.parse(config?.configurable || {});
}