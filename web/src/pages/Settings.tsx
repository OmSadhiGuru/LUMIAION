import { useNavigate } from "react-router-dom";
import { useAuth } from "../lib/AuthContext";
import { useAppSettings } from "../hooks/useLumiData";
import { isSupabaseConfigured } from "../lib/supabase";
import { LogOut, LogIn, GitBranch, Database, Globe } from "lucide-react";

export default function Settings() {
  const { session, signOut } = useAuth();
  const { data: settings } = useAppSettings();
  const navigate = useNavigate();

  const settingsMap = Object.fromEntries((settings ?? []).map((s) => [s.setting_key, s.setting_value]));

  return (
    <div className="pt-6 sm:pt-10">
      <h1 className="font-display text-2xl font-semibold sm:text-3xl">Settings</h1>

      <section className="glass mt-4 rounded-2xl p-4">
        <h2 className="font-display text-sm font-semibold text-white/80">Account</h2>
        {session ? (
          <div className="mt-2 flex items-center justify-between text-sm">
            <span className="text-white/70">{session.user.email}</span>
            <button
              onClick={async () => {
                await signOut();
                navigate("/");
              }}
              className="flex items-center gap-1 rounded-full border border-white/10 px-3 py-1.5 text-xs text-white/70 hover:bg-white/10"
            >
              <LogOut size={14} /> Sign out
            </button>
          </div>
        ) : (
          <div className="mt-2 flex items-center justify-between text-sm">
            <span className="text-white/50">Not signed in</span>
            <button
              onClick={() => navigate("/login")}
              className="flex items-center gap-1 rounded-full bg-nebula px-3 py-1.5 text-xs font-medium"
            >
              <LogIn size={14} /> Sign in
            </button>
          </div>
        )}
      </section>

      <section className="glass mt-4 rounded-2xl p-4">
        <h2 className="font-display text-sm font-semibold text-white/80">Sync preferences</h2>
        <div className="mt-2 space-y-2 text-sm text-white/70">
          <Row label="Timezone" value={String(settingsMap.timezone ?? "—")} />
          <Row label="Supabase sync" value={settingsMap.supabase_sync_enabled ? "Enabled" : "Disabled"} />
          <Row label="Notion sync" value={settingsMap.notion_sync_enabled ? "Enabled" : "Disabled"} />
          <Row label="End-of-day sync" value={String(settingsMap.end_of_day_sync_time ?? "—")} />
        </div>
      </section>

      <section className="glass mt-4 rounded-2xl p-4">
        <h2 className="font-display text-sm font-semibold text-white/80">Connections</h2>
        <div className="mt-2 space-y-2 text-sm text-white/70">
          <Row
            label={
              <span className="flex items-center gap-2">
                <Database size={14} /> Supabase
              </span>
            }
            value={isSupabaseConfigured ? "Connected" : "Not configured"}
          />
          <Row
            label={
              <span className="flex items-center gap-2">
                <GitBranch size={14} /> GitHub
              </span>
            }
            value="OmSadhiGuru/LUMIAION"
          />
          <Row
            label={
              <span className="flex items-center gap-2">
                <Globe size={14} /> Deployment
              </span>
            }
            value="Replit"
          />
        </div>
      </section>

      <p className="mt-6 text-center text-xs text-white/30">LUMIAION · Luminary Brain · v0.1</p>
    </div>
  );
}

function Row({ label, value }: { label: React.ReactNode; value: string }) {
  return (
    <div className="flex items-center justify-between">
      <span>{label}</span>
      <span className="text-white/40">{value}</span>
    </div>
  );
}
