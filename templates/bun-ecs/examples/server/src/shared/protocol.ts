import { z } from "zod";

// RULE 8 (ECS_RULES.md): the client is a liar. Every inbound WebSocket
// message is Zod-validated before it becomes a TickInput — never trust
// position/health/cooldowns reported by the client.

export const MoveSchema = z.object({
  type: z.literal("MOVE"),
  entityId: z.string().uuid(),
  x: z.number(),
  z: z.number(),
});

export const AttackSchema = z.object({
  type: z.literal("ATTACK"),
  entityId: z.string().uuid(),
  targetId: z.string().uuid(),
});

export const ClientMessageSchema = z.discriminatedUnion("type", [MoveSchema, AttackSchema]);

export type ClientMessage = z.infer<typeof ClientMessageSchema>;
