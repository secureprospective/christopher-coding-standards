import { readFileSync } from "node:fs";

// Check the consumer's pin, not a second hard-coded version. No download or shell.
const manifest = JSON.parse(readFileSync(new URL("../package.json", import.meta.url), "utf8"));
const pin = manifest.packageManager;
const actual = (process.env.npm_config_user_agent ?? "").split(" ")[0];

if (typeof pin !== "string" || !pin.startsWith("pnpm@")) {
  process.stderr.write("package.json must declare a pnpm packageManager pin.\n");
  process.exit(1);
}

// Corepack pins may append a +sha... integrity suffix; user agents omit it.
const expected = pin.split("+")[0].replace("@", "/");
if (actual !== expected) {
  process.stderr.write(
    "Use the pnpm version declared in package.json; keep pnpm-lock.yaml frozen.\n",
  );
  process.exit(1);
}
