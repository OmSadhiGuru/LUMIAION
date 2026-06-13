import ModuleHeader from "../../components/ModuleHeader";
import { StatCard, EmptyState } from "../../components/Cards";
import { getModule } from "../../lib/modules";
import { useAgentSessions } from "../../hooks/useLumiData";
import { useAuth } from "../../lib/AuthContext";

const mod = getModule("agents")!;

export default function AgentOS() {
  const { session } = useAuth();
  const { data: sessions, loading } = useAgentSessions();

  const totalPulses = sessions?.reduce((sum, s) => sum + (s.pulse_count ?? 0), 0) ?? 0;
  const uniqueAgents = new Set(sessions?.map((s) => s.agent_id)).size;

  return (
    <div>
      <ModuleHeader module={mod} />

      {!session ? (
        <EmptyState
          title="Sign in to view agent activity"
          description="agent_sessions tracks every conversation, activated node and pulse across LUMIAION's agent hierarchy."
        />
      ) : (
        <>
          <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3">
            <StatCard label="Sessions" value={sessions?.length ?? 0} />
            <StatCard label="Active agents" value={uniqueAgents} />
            <StatCard label="Total pulses" value={totalPulses} />
          </div>

          {loading ? (
            <p className="mt-6 text-sm text-white/50">Listening for pulses...</p>
          ) : sessions && sessions.length > 0 ? (
            <div className="mt-6 space-y-2">
              {sessions.map((s) => (
                <div key={s.id} className="glass rounded-2xl p-4 text-sm">
                  <div className="flex items-center justify-between">
                    <span className="font-display font-semibold">{s.agent_id}</span>
                    <span className="text-xs text-white/40">{s.session_date}</span>
                  </div>
                  <div className="mt-1 text-xs text-white/50">
                    {s.nodes_activated?.length ?? 0} nodes · {s.edges_activated?.length ?? 0} edges ·{" "}
                    {s.pulse_count ?? 0} pulses
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState
              title="No agent sessions yet"
              description="As LUMIAION's agents run, each session, node activation and pulse will appear here in real time."
            />
          )}
        </>
      )}
    </div>
  );
}
