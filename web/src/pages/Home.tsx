import { useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { MessageCircle, LogIn } from "lucide-react";
import BrainOrb from "../components/BrainOrb";
import ChatPanel from "../components/ChatPanel";
import { MODULES } from "../lib/modules";
import { useAuth } from "../lib/AuthContext";
import { useTodayCache } from "../hooks/useLumiData";

function greeting() {
  const hour = new Date().getHours();
  if (hour < 5) return "Still awake, seeker?";
  if (hour < 12) return "Good morning";
  if (hour < 18) return "Good afternoon";
  return "Good evening";
}

export default function Home() {
  const [chatOpen, setChatOpen] = useState(false);
  const { session, loading } = useAuth();
  const { data: cache } = useTodayCache();

  const activity = cache?.agent_activity as Record<string, number> | undefined;

  return (
    <div className="pt-4 sm:pt-8">
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center"
      >
        <p className="text-sm uppercase tracking-[0.3em] text-white/40">{greeting()}</p>
        <h1 className="mt-1 font-display text-3xl font-semibold sm:text-4xl">
          You are <span className="text-nebula">LUMIAION</span>
        </h1>
        <p className="mx-auto mt-2 max-w-md text-sm text-white/60">
          Your consciousness, knowledge and wisdom — mapped as one living system. Tap a node to step inside.
        </p>
      </motion.div>

      <div className="mt-8 flex justify-center">
        <BrainOrb activity={activity} />
      </div>

      <div className="mt-6 flex justify-center">
        <button
          onClick={() => setChatOpen(true)}
          className="flex items-center gap-2 rounded-full bg-nebula px-5 py-3 text-sm font-semibold text-white shadow-2xl shadow-nebula/40 transition hover:brightness-110"
        >
          <MessageCircle size={18} />
          Ask LUMIAION
        </button>
      </div>

      {!loading && !session && (
        <div className="glass mx-auto mt-6 flex max-w-md items-center justify-between gap-3 rounded-2xl px-4 py-3 text-sm">
          <span className="text-white/70">Sign in to sync your real data across this brain.</span>
          <Link to="/login" className="flex items-center gap-1 rounded-full bg-nebula px-3 py-1.5 text-xs font-medium">
            <LogIn size={14} /> Sign in
          </Link>
        </div>
      )}

      {cache && (
        <div className="glass mx-auto mt-6 grid max-w-md grid-cols-3 gap-3 rounded-2xl px-4 py-3 text-center text-xs">
          <Stat label="Moon" value={cache.moon_phase ?? "—"} />
          <Stat label="Goals" value={`${cache.goals_completed}/${cache.goals_active || cache.goals_completed}`} />
          <Stat label="Journal" value={String(cache.journal_count)} />
        </div>
      )}

      <div className="mt-10 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
        {MODULES.map((mod, i) => (
          <motion.div
            key={mod.id}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.05 * i }}
          >
            <Link
              to={mod.path}
              className="glass group flex h-full flex-col gap-2 rounded-2xl p-4 transition hover:-translate-y-1 hover:border-white/20"
              style={{ boxShadow: `0 0 0 1px ${mod.color}1a` }}
            >
              <mod.icon size={22} style={{ color: mod.color }} />
              <div className="font-display text-sm font-semibold">{mod.label}</div>
              <div className="text-xs text-white/50">{mod.tagline}</div>
            </Link>
          </motion.div>
        ))}
      </div>

      <ChatPanel open={chatOpen} onClose={() => setChatOpen(false)} />
    </div>
  );
}

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="font-display text-base font-semibold text-white">{value}</div>
      <div className="text-white/40">{label}</div>
    </div>
  );
}
