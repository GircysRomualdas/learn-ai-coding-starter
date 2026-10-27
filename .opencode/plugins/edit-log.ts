import { appendFile, mkdir } from "node:fs/promises";
import { dirname, join } from "node:path";

import { Plugin } from "@opencode/plugin";

const FILE_CHANGING_TOOLS = ["edit", "write", "patch"];

export default Plugin.define({
  id: "edit-log",
  setup: async (ctx) => {
    const logPath = join(ctx.location.directory, "logs/plugin-tools.log");

    await ctx.tool.hook("execute.after", async (event) => {
      if (event.status !== "completed") return;
      if (!FILE_CHANGING_TOOLS.includes(event.tool)) return;

      const entry = {
        timestamp: new Date().toISOString(),
        sessionID: event.sessionID,
        tool: event.tool,
        status: event.status,
      };

      try {
        await mkdir(dirname(logPath), { recursive: true });
        await appendFile(logPath, JSON.stringify(entry) + "\n");
      } catch (error) {
        console.error("could not write file change log:", error);
      }
    });
  },
});
