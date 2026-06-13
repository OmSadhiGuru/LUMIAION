import ModuleHeader from "../../components/ModuleHeader";
import { StatCard, SeedCard, EmptyState } from "../../components/Cards";
import { getModule } from "../../lib/modules";
import { useNatalChart, useTodayCache } from "../../hooks/useLumiData";
import { useAuth } from "../../lib/AuthContext";
import { BookHeart, Moon, NotebookPen, Sparkle } from "lucide-react";

const mod = getModule("life")!;

export default function LifeOS() {
  const { session } = useAuth();
  const { data: chart, loading: chartLoading } = useNatalChart();
  const { data: cache } = useTodayCache();

  return (
    <div>
      <ModuleHeader module={mod} />

      {!session ? (
        <EmptyState
          title="Sign in to see your natal chart & journal"
          description="Your birth data, planetary placements, daily journal and moon phase live in Supabase, scoped to your account."
        />
      ) : chartLoading ? (
        <p className="mt-6 text-sm text-white/50">Reading the stars...</p>
      ) : chart ? (
        <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3">
          <StatCard label="Sun" value={chart.sun_sign ?? "—"} />
          <StatCard label="Moon" value={chart.moon_sign ?? "—"} />
          <StatCard label="Rising" value={chart.rising_sign ?? "—"} />
          <StatCard label="Birth date" value={chart.birth_date} />
          <StatCard label="Location" value={chart.birth_location} />
          <StatCard label="Today's moon" value={cache?.moon_phase ?? "—"} />
        </div>
      ) : (
        <EmptyState
          title="No natal chart yet"
          description="Once your birth data is saved to the natal_chart table, your placements will glow here."
        />
      )}

      <div className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2">
        <SeedCard
          icon={NotebookPen}
          title="Daily journal"
          description={
            cache
              ? `${cache.journal_count} entr${cache.journal_count === 1 ? "y" : "ies"} logged today.`
              : "Reflections sync here from your daily cache."
          }
          color={mod.color}
        />
        <SeedCard
          icon={Sparkle}
          title="Essence snapshot"
          description="A living read of your current state — mood, focus and alignment, drawn from daily_cache.essence_snapshot."
          color={mod.color}
        />
        <SeedCard
          icon={Moon}
          title="Lunar rhythm"
          description="Moon phase tracking informs rituals, rest and timing across every other OS."
          color={mod.color}
        />
        <SeedCard
          icon={BookHeart}
          title="Inner archive"
          description="Long-form reflections, breakthroughs and the story of your becoming."
          color={mod.color}
        />
      </div>
    </div>
  );
}
