import { spawn } from "node:child_process";

import { Plugin } from "@opencode/plugin";

interface SlopResult {
  stdout: string;
  stderr: string;
  exitCode: number;
}

function runSlop(path: string, cwd: string): Promise<SlopResult> {
  return new Promise((resolve, reject) => {
    const child = spawn("uv", ["run", "--no-active", "sloperator.py", path], { cwd });
    let stdout = "";
    let stderr = "";

    child.stdout?.setEncoding("utf8");
    child.stderr?.setEncoding("utf8");
    child.stdout?.on("data", (chunk: string) => {
      stdout += chunk;
    });
    child.stderr?.on("data", (chunk: string) => {
      stderr += chunk;
    });
    child.on("error", reject);
    child.on("close", (code) => {
      resolve({ stdout, stderr, exitCode: code ?? -1 });
    });
  });
}

export default Plugin.define({
  id: "run-slop",
  setup: async (ctx) => {
    const directory = ctx.location.directory;

    await ctx.tool.transform((tools) => {
      tools.add({
        name: "run_slop",
        description:
          "Run a SlopLang (.slop) file with the Sloperator interpreter and return its stdout, stderr, and exit code as JSON.",
        input: {
          type: "object",
          properties: {
            path: {
              type: "string",
              description: "Path to the .slop file, relative to the project root.",
            },
          },
          required: ["path"],
          additionalProperties: false,
        },
        output: {
          type: "object",
          properties: {
            stdout: { type: "string" },
            stderr: { type: "string" },
            exitCode: { type: "number" },
          },
          required: ["stdout", "stderr", "exitCode"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async (input) => {
          const { path } = input as { path: string };
          const result = await runSlop(path, directory);
          return {
            output: result,
            content: JSON.stringify(result, null, 2),
          };
        },
      });
    });

    await ctx.tool.transform((tools) => {
      tools.update("run_slop", (tool) => {
        tool.description +=
          "\nUse this tool to run individual .slop examples when checking language behavior. Use the test suite for regression testing.";
      });
    });
  },
});
