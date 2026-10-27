import { spawn } from "node:child_process";
import { readdir } from "node:fs/promises";
import { join } from "node:path";

import { Plugin } from "@opencode/plugin";

interface ExampleResult {
  name: string;
  exitCode: number;
  firstLine: string;
}

interface ProcessResult {
  stdout: string;
  exitCode: number;
}

function runExample(file: string, cwd: string): Promise<ProcessResult> {
  return new Promise((resolve, reject) => {
    const child = spawn("uv", ["run", "--no-active", "sloperator.py", file], { cwd });
    let stdout = "";

    child.stdout?.setEncoding("utf8");
    child.stderr?.setEncoding("utf8");
    child.stdout?.on("data", (chunk: string) => {
      stdout += chunk;
    });
    child.stderr?.resume();
    child.on("error", reject);
    child.on("close", (code) => {
      resolve({ stdout, exitCode: code ?? -1 });
    });
  });
}

function firstLineOf(stdout: string): string {
  return stdout.split("\n")[0];
}

export default Plugin.define({
  id: "example-outputs",
  setup: async (ctx) => {
    const directory = ctx.location.directory;
    const examplesDir = join(directory, "examples");

    await ctx.tool.transform((tools) => {
      tools.add({
        name: "example_outputs",
        description:
          "Run every examples/*.slop file and return each example's filename, exit code, and first output line.",
        input: {
          type: "object",
          properties: {},
          additionalProperties: false,
        },
        output: {
          type: "object",
          properties: {
            examples: {
              type: "array",
              items: {
                type: "object",
                properties: {
                  name: { type: "string" },
                  exitCode: { type: "number" },
                  firstLine: { type: "string" },
                },
                required: ["name", "exitCode", "firstLine"],
                additionalProperties: false,
              },
            },
          },
          required: ["examples"],
          additionalProperties: false,
        },
        options: { codemode: false },
        execute: async () => {
          const files = (await readdir(examplesDir))
            .filter((file) => file.endsWith(".slop"))
            .sort();

          const examples: ExampleResult[] = [];
          for (const file of files) {
            const result = await runExample(join(examplesDir, file), directory);
            examples.push({
              name: file,
              exitCode: result.exitCode,
              firstLine: firstLineOf(result.stdout),
            });
          }

          return {
            output: { examples },
            content: JSON.stringify({ examples }, null, 2),
          };
        },
      });
    });
  },
});
