export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    if (request.method !== "POST") return new Response("method", { status: 405 });
    let body: unknown;
    try {
      body = await request.json();
    } catch {
      return new Response("invalid JSON", { status: 400 });
    }
    if (
      typeof body !== "object" ||
      body === null ||
      !("value" in body) ||
      typeof body.value !== "string" ||
      body.value.length === 0
    )
      return new Response("invalid value", { status: 400 });
    try {
      await env.KV.put("message", body.value);
    } catch {
      return new Response("storage unavailable", { status: 503 });
    }
    return new Response("stored", { status: 201 });
  },
} satisfies ExportedHandler<Env>;
