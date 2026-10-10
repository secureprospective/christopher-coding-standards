import { z } from "zod";

// Shape boundary only; default Zod objects strip unknown fields here.
// Validation does not grant entity ownership/action permission or enforce
// movement range/rate. Callers must validate before effects and own those rules.

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
