import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../lib/AuthContext";
import { isSupabaseConfigured } from "../lib/supabase";

export default function Login() {
  const { signInWithPassword, signUp, session } = useAuth();
  const navigate = useNavigate();
  const [mode, setMode] = useState<"signin" | "signup">("signin");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  if (session) {
    navigate("/");
  }

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setBusy(true);
    setMessage(null);

    const result = mode === "signin" ? await signInWithPassword(email, password) : await signUp(email, password);

    setBusy(false);
    if (result.error) {
      setMessage(result.error);
    } else if (mode === "signup") {
      setMessage("Account created. Check your email to confirm, then sign in.");
    } else {
      navigate("/");
    }
  };

  return (
    <div className="flex min-h-[70vh] items-center justify-center pt-10">
      <div className="glass w-full max-w-sm rounded-3xl p-6">
        <h1 className="font-display text-xl font-semibold">
          {mode === "signin" ? "Welcome back" : "Create your account"}
        </h1>
        <p className="mt-1 text-sm text-white/50">
          This is a single-owner brain — sign in to unlock your synced data.
        </p>

        {!isSupabaseConfigured && (
          <p className="mt-4 rounded-xl bg-ember/10 px-3 py-2 text-xs text-ember">
            Supabase isn't configured. Set VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY in web/.env.
          </p>
        )}

        <form onSubmit={submit} className="mt-4 space-y-3">
          <input
            type="email"
            required
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm outline-none placeholder:text-white/40 focus:border-nebula/60"
          />
          <input
            type="password"
            required
            minLength={6}
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-2.5 text-sm outline-none placeholder:text-white/40 focus:border-nebula/60"
          />
          <button
            type="submit"
            disabled={busy}
            className="w-full rounded-xl bg-nebula py-2.5 text-sm font-semibold text-white transition disabled:opacity-50"
          >
            {mode === "signin" ? "Sign in" : "Sign up"}
          </button>
        </form>

        {message && <p className="mt-3 text-xs text-white/70">{message}</p>}

        <button
          onClick={() => setMode(mode === "signin" ? "signup" : "signin")}
          className="mt-4 text-xs text-white/50 underline-offset-2 hover:underline"
        >
          {mode === "signin" ? "Need an account? Sign up" : "Already have an account? Sign in"}
        </button>
      </div>
    </div>
  );
}
