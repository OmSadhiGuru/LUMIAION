import ModuleHeader from "../../components/ModuleHeader";
import { StatCard, SeedCard, EmptyState } from "../../components/Cards";
import { getModule } from "../../lib/modules";
import { useTodayCache } from "../../hooks/useLumiData";
import { useAuth } from "../../lib/AuthContext";
import { Coins, PiggyBank, TrendingUp, Wind } from "lucide-react";

const mod = getModule("finance")!;

export default function FinanceOS() {
  const { session } = useAuth();
  const { data: cache, loading } = useTodayCache();
  const finance = (cache?.finance_log ?? {}) as Record<string, unknown>;
  const hasEntries = Object.keys(finance).length > 0;

  return (
    <div>
      <ModuleHeader module={mod} />

      {!session ? (
        <EmptyState
          title="Sign in to view your finance log"
          description="Wealth tracking flows from daily_cache.finance_log into the Vortex trading layer."
        />
      ) : loading ? (
        <p className="mt-6 text-sm text-white/50">Counting the flow...</p>
      ) : (
        <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3">
          <StatCard label="Today's entries" value={hasEntries ? Object.keys(finance).length : 0} />
          <StatCard label="Synced" value={cache?.synced_to_supabase ? "Yes" : "Pending"} />
        </div>
      )}

      <div className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2">
        <SeedCard
          icon={Wind}
          title="The Vortex"
          description="Your active trading layer — positions, signals and the energetic flow of capital."
          color={mod.color}
        />
        <SeedCard
          icon={TrendingUp}
          title="Income streams"
          description="Every revenue source from Business OS rolled up into one wealth picture."
          color={mod.color}
        />
        <SeedCard
          icon={PiggyBank}
          title="Reserves"
          description="Savings, runway and the safety net beneath every bold move."
          color={mod.color}
        />
        <SeedCard
          icon={Coins}
          title="Daily ledger"
          description="A lightweight log of spending and earning, captured without friction."
          color={mod.color}
        />
      </div>
    </div>
  );
}
