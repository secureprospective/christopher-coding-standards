import { env, exports } from "cloudflare:workers";
import { expect, it } from "vitest";
import worker from "./index";

it("actual workerd binding and integration effect", async () => {
  const response = await exports.default.fetch("https://example.com/", {
    method: "POST",
    body: JSON.stringify({ value: "hello" }),
  });
  expect(response.status).toBe(201);
  expect(await env.KV.get("message")).toBe("hello");
});
it("invalid shape preserves prior state", async () => {
  await env.KV.put("message", "prior");
  const response = await exports.default.fetch("https://example.com/", {
    method: "POST",
    body: JSON.stringify({ value: 42 }),
  });
  expect(response.status).toBe(400);
  expect(await env.KV.get("message")).toBe("prior");
});
it("malformed JSON preserves state", async () => {
  await env.KV.put("message", "prior");
  const response = await exports.default.fetch("https://example.com/", {
    method: "POST",
    body: "{",
  });
  expect(response.status).toBe(400);
  expect(await env.KV.get("message")).toBe("prior");
});
it("method rejects before state changes", async () => {
  await env.KV.put("message", "prior");
  const response = await exports.default.fetch("https://example.com/");
  expect(response.status).toBe(405);
  expect(await env.KV.get("message")).toBe("prior");
});
it("effect failure is explicit, not success", async () => {
  const badEnv = {
    ...env,
    KV: {
      ...env.KV,
      put: async () => {
        throw new Error("fixture storage failure");
      },
    },
  };
  const response = await worker.fetch(
    new Request("https://example.com/", {
      method: "POST",
      body: JSON.stringify({ value: "hello" }),
    }),
    badEnv,
  );
  expect(response.status).toBe(503);
  expect(await response.text()).toBe("storage unavailable");
});
