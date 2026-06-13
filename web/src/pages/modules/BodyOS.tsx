import ModuleHeader from "../../components/ModuleHeader";
import { StatCard, SeedCard, EmptyState } from "../../components/Cards";
import { getModule } from "../../lib/modules";
import { useTodayCache } from "../../hooks/useLumiData";
import { useAuth } from "../../lib/AuthContext";
import { Activity, BedDouble, Flame, HeartPulse } from "lucide-react";

const mod = getModule("body")!;

export default function BodyOS() {
  const { session } = useAuth();
  const { data: cache, loading } = useTodayCache();
  const fitness = cache?.fitness_log as Record<string, unknown> | undefined;

  return (
    <div>
      <ModuleHeader module={mod} />

      {!session ? (
        <EmptyState
          title="Sign in to view today's training data"
          description="Readiness scores and training logs sync from daily_cache.fitness_log and fitness_readiness."
        />
      ) : loading ? (
        <p className="mt-6 text-sm text-white/50">Checking vitals...</p>
      ) : (
        <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3">
          <StatCard
            label="Readiness"
            value={cache?.fitness_readiness != null ? `${cache.fitness_readiness}%` : "—"}
          />
          <StatCard label="Logged today" value={fitness && Object.keys(fitness).length > 0 ? "Yes" : "Not yet"} />
          <StatCard label="Moon phase" value={cache?.moon_phase ?? "—"} />
        </div>
      )}

      <div className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2">
        <SeedCard
          icon={Activity}
          title="Training log"
          description="Sessions, sets, reps and intensity — the raw signal feeding your readiness score."
          color={mod.color}
        />
        <SeedCard
          icon={HeartPulse}
          title="Readiness score"
          description="A daily composite of sleep, recovery and load, scored 0-100."
          color={mod.color}
        />
        <SeedCard
          icon={BedDouble}
          title="Recovery"
          description="Sleep quality and rest days, tracked alongside training to prevent burnout."
          color={mod.color}
        />
        <SeedCard
          icon={Flame}
          title="Streaks & momentum"
          description="Consistency over intensity — your longest streaks live here."
          color={mod.color}
        />
      </div>
    </div>
  );
}
