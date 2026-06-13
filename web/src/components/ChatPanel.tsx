import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, X, Sparkles, Loader2 } from "lucide-react";
import { supabase, isSupabaseConfigured } from "../lib/supabase";
import type { ChatMessage } from "../lib/types";

interface ChatPanelProps {
  open: boolean;
  onClose: () => void;
}

const BRAIN_OPTIONS = [
  { id: "auto", label: "LUMIAION Auto", provider: "auto" },
  { id: "claude", label: "Claude (Anthropic)", provider: "anthropic" },
  { id: "gpt", label: "GPT (OpenAI)", provider: "openai" },
] as const;

const FUNCTION_NAME = import.meta.env.VITE_LUMIAION_BRAIN_FUNCTION || "lumiaion-brain";

const INTRO: ChatMessage = {
  role: "assistant",
  content:
    "I'm LUMIAION — your luminary brain. Ask me anything about your knowledge, life, business, finance, body or creative work, and I'll route the thought through whichever mind fits best.",
};

export default function ChatPanel({ open, onClose }: ChatPanelProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([INTRO]);
  const [input, setInput] = useState("");
  const [brain, setBrain] = useState<(typeof BRAIN_OPTIONS)[number]["id"]>("auto");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, open]);

  const send = async () => {
    const text = input.trim();
    if (!text || loading) return;

    const nextMessages: ChatMessage[] = [...messages, { role: "user", content: text }];
    setMessages(nextMessages);
    setInput("");
    setError(null);
    setLoading(true);

    const provider = BRAIN_OPTIONS.find((b) => b.id === brain)?.provider ?? "auto";

    try {
      if (!isSupabaseConfigured) {
        throw new Error(
          "Supabase isn't configured yet — set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY in web/.env",
        );
      }

      const { data, error: fnError } = await supabase.functions.invoke(FUNCTION_NAME, {
        body: {
          provider,
          messages: nextMessages.map(({ role, content }) => ({ role, content })),
        },
      });

      if (fnError) throw fnError;

      const reply: string =
        data?.reply ?? "LUMIAION is realigning to the source. Please try again shortly.";
      const usedModel: string | undefined = data?.model;

      setMessages((prev) => [...prev, { role: "assistant", content: reply, model: usedModel }]);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Something went wrong.";
      setError(message);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "I couldn't reach my full intelligence just now. Once the lumiaion-brain Edge Function and its API keys are configured, I'll respond fully.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-30 flex items-end justify-center bg-black/60 backdrop-blur-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
        >
          <motion.div
            className="glass safe-bottom flex h-[80vh] w-full max-w-2xl flex-col rounded-t-3xl border-white/10 p-4 sm:h-[70vh]"
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "100%" }}
            transition={{ type: "spring", damping: 28, stiffness: 260 }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between pb-3">
              <div className="flex items-center gap-2 font-display text-lg font-semibold">
                <Sparkles size={18} className="text-nebula" />
                LUMIAION
              </div>
              <div className="flex items-center gap-2">
                <select
                  value={brain}
                  onChange={(e) => setBrain(e.target.value as typeof brain)}
                  className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-white/80 outline-none"
                >
                  {BRAIN_OPTIONS.map((b) => (
                    <option key={b.id} value={b.id} className="bg-deep">
                      {b.label}
                    </option>
                  ))}
                </select>
                <button
                  onClick={onClose}
                  className="rounded-full p-1.5 text-white/60 transition hover:bg-white/10 hover:text-white"
                  aria-label="Close chat"
                >
                  <X size={18} />
                </button>
              </div>
            </div>

            <div ref={scrollRef} className="flex-1 space-y-3 overflow-y-auto pb-3 pr-1">
              {messages.map((m, i) => (
                <div
                  key={i}
                  className={`max-w-[85%] rounded-2xl px-4 py-2 text-sm leading-relaxed ${
                    m.role === "user"
                      ? "ml-auto bg-nebula/30 text-white"
                      : "glass border-white/5 text-white/90"
                  }`}
                >
                  {m.content}
                  {m.model && <div className="mt-1 text-[10px] uppercase tracking-wide text-white/40">{m.model}</div>}
                </div>
              ))}
              {loading && (
                <div className="glass flex w-fit items-center gap-2 rounded-2xl px-4 py-2 text-sm text-white/70">
                  <Loader2 size={14} className="animate-spin" />
                  Thinking...
                </div>
              )}
              {error && <div className="text-xs text-ember">{error}</div>}
            </div>

            <form
              className="flex items-center gap-2 border-t border-white/10 pt-3"
              onSubmit={(e) => {
                e.preventDefault();
                send();
              }}
            >
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask LUMIAION anything..."
                className="flex-1 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm outline-none placeholder:text-white/40 focus:border-nebula/60"
              />
              <button
                type="submit"
                disabled={loading || !input.trim()}
                className="rounded-full bg-nebula p-2.5 text-white transition disabled:opacity-40"
                aria-label="Send"
              >
                <Send size={16} />
              </button>
            </form>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
