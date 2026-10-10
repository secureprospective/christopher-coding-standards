import { describe, expect, it } from "bun:test";
import { CreateUserSchema, handleCreateUser, handleCreateUserAsync } from "./example";

const valid = { email: "user@example.com", name: "Chris", role: "member" } as const;
const invalid = [
  null,
  undefined,
  [],
  "user",
  {},
  { ...valid, email: "invalid" },
  { ...valid, name: "" },
  { ...valid, name: "x".repeat(101) },
  { ...valid, role: "owner" },
  { ...valid, extra: true },
  { ...valid, avatarUrl: "not-a-url" },
  { ...valid, email: 42 },
];

describe("CreateUser boundary", () => {
  it("accepts each declared role without treating it as authorization", () => {
    for (const role of ["admin", "member", "viewer"] as const) {
      const input = { ...valid, role };
      expect(handleCreateUser(input)).toEqual(input);
    }
  });

  it("preserves optional URLs and both name limits", async () => {
    for (const name of ["x", "x".repeat(100)]) {
      const input = { ...valid, name, avatarUrl: "https://example.com/avatar.png" };
      expect(handleCreateUser(input)).toEqual(input);
      expect(await handleCreateUserAsync(input)).toEqual(input);
    }
  });

  it.each(
    invalid.map((input) => [input]),
  )("rejects invalid input %# in both parser paths", async (input) => {
    expect(CreateUserSchema.safeParse(input).success).toBe(false);
    expect(handleCreateUser(input)).toBeNull();
    expect(await handleCreateUserAsync(input)).toBeNull();
  });

  it("lets a caller stop before effects and does not mutate inputs", () => {
    const accepted: unknown[] = [];
    const receive = (raw: unknown) => {
      const parsed = handleCreateUser(raw);
      if (parsed !== null) accepted.push(parsed);
    };
    const rejected = { ...valid, extra: true };
    const before = structuredClone(rejected);
    receive(rejected);
    expect(rejected).toEqual(before);
    expect(accepted).toEqual([]);
    receive(valid);
    expect(accepted).toEqual([valid]);
    expect(valid).toEqual({ email: "user@example.com", name: "Chris", role: "member" });
  });
});
