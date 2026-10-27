import { appendFile, mkdir } from "node:fs/promises";
import { dirname, join } from "node:path";

import { Plugin } from "@opencode/plugin";

const PLAYGROUND_COMMAND = "playground/server.py";

function commandOf(input: unknown): string | undefined {
  if (typeof input !== "object" || input === null) return undefined;
  const { command } = input as { command?: unknown };
  return typeof command === "string" ? command : undefined;
}

export default Plugin.define({
  id: "playground-log",
  setup: async (ctx) => {
    const logPath = join(ctx.location.directory, "logs/plugin-playground.log");

    await ctx.tool.hook("execute.before", async (event) => {
      if (event.tool !== "shell") return;

      const command = commandOf(event.input);
      if (!command || !command.includes(PLAYGROUND_COMMAND)) return;

      const entry = {
        timestamp: new Date().toISOString(),
        sessionID: event.sessionID,
        event: "playground shell request",
        command,
      };

      try {
        await mkdir(dirname(logPath), { recursive: true });
        await appendFile(logPath, JSON.stringify(entry) + "\n");
      } catch (error) {
        console.error("could not write playground shell request log:", error);
      }
    });
  },
});
