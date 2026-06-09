/**
 * Boundary validation pattern using Zod v4.
 *
 * Use this pattern at every system boundary:
 *   - HTTP request bodies and query parameters
 *   - File ingestion (CSV, JSON uploads)
 *   - IPC / message queue payloads
 *   - External API responses before use
 *   - CLI arguments
 *
 * RULE: Never pass raw external input into business logic.
 * Parse it through a schema first. If it fails, reject it at the boundary.
 */

import { z } from "zod";

// --- Define the schema ---
// .strict() rejects any fields not declared here.
// Without .strict(), extra fields pass silently — an attack vector and a bug source.
const CreateUserSchema = z
  .object({
    email: z.string().email(),
    name: z.string().min(1).max(100),
    role: z.enum(["admin", "member", "viewer"]),
    // Optional field: must be a valid URL if present.
    avatarUrl: z.string().url().optional(),
  })
  .strict();

// --- Infer the TypeScript type from the schema ---
// Never write a separate type manually. Change the schema; the type updates automatically.
type CreateUserInput = z.infer<typeof CreateUserSchema>;

// --- Parse at the boundary using safeParse ---
// safeParse returns { success: true, data } or { success: false, error }.
// Use safeParse, not parse. parse throws — forcing try/catch everywhere.
// safeParse returns a discriminated union — TypeScript handles it cleanly.
function handleCreateUser(rawBody: unknown): CreateUserInput | null {
  const result = CreateUserSchema.safeParse(rawBody);

  if (!result.success) {
    // Log the validation error. Never forward zod error details to external responses
    // — they can leak schema structure to an attacker.
    console.warn("Validation failed:", result.error.flatten());
    return null;
  }

  // result.data is fully typed as CreateUserInput here.
  return result.data;
}

// --- Async boundaries ---
// If your schema uses async refinements or transforms, use safeParseAsync.
async function handleCreateUserAsync(rawBody: unknown): Promise<CreateUserInput | null> {
  const result = await CreateUserSchema.safeParseAsync(rawBody);
  if (!result.success) return null;
  return result.data;
}

export { CreateUserSchema, handleCreateUser, handleCreateUserAsync };
export type { CreateUserInput };
