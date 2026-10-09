import { z } from "zod";

// This protocol rejects unknown fields; other protocols may strip/preserve them.
// A valid role is a shape check, NOT permission to create an admin user.
const CreateUserSchema = z
  .object({
    email: z.string().email(),
    name: z.string().min(1).max(100),
    role: z.enum(["admin", "member", "viewer"]),
    avatarUrl: z.string().url().optional(),
  })
  .strict();

type CreateUserInput = z.infer<typeof CreateUserSchema>;

// Caller must reject null before effects and separately authorize the operation.
// Do not log raw validation errors or echo them into public responses.
function handleCreateUser(rawBody: unknown): CreateUserInput | null {
  const result = CreateUserSchema.safeParse(rawBody);
  return result.success ? result.data : null;
}

// Use the async path when a project's schema has async refinements/transforms.
async function handleCreateUserAsync(rawBody: unknown): Promise<CreateUserInput | null> {
  const result = await CreateUserSchema.safeParseAsync(rawBody);
  return result.success ? result.data : null;
}

export type { CreateUserInput };
export { CreateUserSchema, handleCreateUser, handleCreateUserAsync };
