import ModuleHeader from "../../components/ModuleHeader";
import { StatCard, SeedCard, EmptyState } from "../../components/Cards";
import { getModule } from "../../lib/modules";
import { useTodayCache } from "../../hooks/useLumiData";
import { useAuth } from "../../lib/AuthContext";
import { Archive, BookOpenCheck, GraduationCap, Target } from "lucide-react";

const mod = getModule("knowledge")!;

export default function Knowledge() {
  const { session } = useAuth();
  const { data: cache, loading } = useTodayCache();
  const goals = cache?.goals_snapshot ?? [];

  return (
    <div>
      <ModuleHeader module={mod} />

      {!session ? (
        <EmptyState
          title="Sign in to see your goals & progress"
          description="Active and completed goals sync from daily_cache.goals_snapshot."
        />
      ) : loading ? (
        <p className="mt-6 text-sm text-white/50">Indexing your mind...</p>
      ) : (
        <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3">
          <StatCard label="Active goals" value={cache?.goals_active ?? 0} />
          <StatCard label="Completed today" value={cache?.goals_completed ?? 0} />
          <StatCard label="Tracked goals" value={goals.length} />
        </div>
      )}

      <div className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2">
        <SeedCard
          icon={GraduationCap}
          title="Subjects"
          description="Every domain you're actively studying — frameworks, courses and core concepts."
          color={mod.color}
        />
        <SeedCard
          icon={BookOpenCheck}
          title="Reading list"
          description="Books, articles and papers — what you're reading, and what it taught you."
          color={mod.color}
        />
        <SeedCard
          icon={Target}
          title="Goals"
          description="The active goals shaping your direction, tracked daily through your cache."
          color={mod.color}
        />
        <SeedCard
          icon={Archive}
          title="Archives"
          description="Completed projects, retired ideas and the wisdom you've already extracted."
          color={mod.color}
        />
      </div>
    </div>
  );
}
