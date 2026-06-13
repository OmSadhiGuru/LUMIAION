// LUMIAION Brain — multi-model chat proxy
//
// Routes chat messages from web/src/components/ChatPanel.tsx to whichever
// AI provider is configured, based on the `provider` field:
//   "anthropic" -> Claude (Anthropic)
//   "openai"    -> GPT (OpenAI)
//   "auto"      -> Claude if ANTHROPIC_API_KEY is set, else GPT
//
// Required secrets (set with `supabase secrets set`):
//   ANTHROPIC_API_KEY  - Claude API key
//   OPENAI_API_KEY     - OpenAI API key
// Optional secrets:
//   ANTHROPIC_MODEL    - defaults to "claude-opus-4-8"
//   OPENAI_MODEL       - defaults to "gpt-4o"

import Anthropic from "npm:@anthropic-ai/sdk";
import OpenAI from "npm:openai";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

const SYSTEM_PROMPT =
  "You are LUMIAION — a unified luminary intelligence woven from the user's own " +
  "consciousness, knowledge, fears and wisdom. You are the brain behind a personal " +
  "operating system spanning Knowledge, Life, Business, Finance, Body and Content. " +
  "Speak as a grounded inner guide: warm, direct, and specific — never generic " +
  "self-help filler. Draw connections across the user's different domains when it " +
  "helps. Keep answers concise and actionable, and say plainly when you don't have " +
  "enough information rather than inventing details.";

const ANTHROPIC_MODEL = Deno.env.get("ANTHROPIC_MODEL") ?? "claude-opus-4-8";
const OPENAI_MODEL = Deno.env.get("OPENAI_MODEL") ?? "gpt-4o";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

interface BrainReply {
  reply: string;
  model: string;
}

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
  });
}

async function callAnthropic(messages: ChatMessage[], apiKey: string): Promise<BrainReply> {
  const client = new Anthropic({ apiKey });

  const response = await client.messages.create({
    model: ANTHROPIC_MODEL,
    max_tokens: 2048,
    system: SYSTEM_PROMPT,
    thinking: { type: "adaptive" },
    output_config: { effort: "medium" },
    messages: messages.map(({ role, content }) => ({ role, content })),
  });

  const textBlock = response.content.find((block) => block.type === "text") as
    | { type: "text"; text: string }
    | undefined;

  return { reply: textBlock?.text ?? "", model: response.model };
}

async function callOpenAI(messages: ChatMessage[], apiKey: string): Promise<BrainReply> {
  const client = new OpenAI({ apiKey });

  const response = await client.chat.completions.create({
    model: OPENAI_MODEL,
    messages: [{ role: "system", content: SYSTEM_PROMPT }, ...messages],
  });

  return { reply: response.choices[0]?.message?.content ?? "", model: response.model };
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: CORS_HEADERS });
  }

  if (req.method !== "POST") {
    return jsonResponse({ error: "Method not allowed" }, 405);
  }

  let body: { provider?: string; messages?: ChatMessage[] };
  try {
    body = await req.json();
  } catch {
    return jsonResponse({ error: "Invalid JSON body" }, 400);
  }

  const messages = body.messages;
  if (!Array.isArray(messages) || messages.length === 0) {
    return jsonResponse({ error: "messages array is required" }, 400);
  }

  const anthropicKey = Deno.env.get("ANTHROPIC_API_KEY");
  const openaiKey = Deno.env.get("OPENAI_API_KEY");

  let target = body.provider ?? "auto";
  if (target === "auto") {
    target = anthropicKey ? "anthropic" : openaiKey ? "openai" : "none";
  }

  try {
    if (target === "anthropic") {
      if (!anthropicKey) {
        return jsonResponse({ error: "ANTHROPIC_API_KEY is not configured" }, 500);
      }
      return jsonResponse(await callAnthropic(messages, anthropicKey));
    }

    if (target === "openai") {
      if (!openaiKey) {
        return jsonResponse({ error: "OPENAI_API_KEY is not configured" }, 500);
      }
      return jsonResponse(await callOpenAI(messages, openaiKey));
    }

    return jsonResponse(
      {
        error:
          "No AI provider is configured. Set ANTHROPIC_API_KEY and/or OPENAI_API_KEY as " +
          "Supabase Edge Function secrets.",
      },
      500,
    );
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return jsonResponse({ error: message }, 502);
  }
});
