import { useEffect, useState } from "react";
import { supabase, isSupabaseConfigured } from "../lib/supabase";
import { useAuth } from "../lib/AuthContext";
import { CURRENT_USER_ID, type AgentSession, type AppSetting, type DailyCache, type NatalChart } from "../lib/types";

interface QueryState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

/** Generic loader: only queries Supabase once a session exists (RLS requires `authenticated`). */
function useLumiQuery<T>(
  fetcher: () => PromiseLike<{ data: T | null; error: { message: string } | null }>,
  deps: unknown[],
): QueryState<T> {
  const { session, loading: authLoading } = useAuth();
  const [state, setState] = useState<QueryState<T>>({ data: null, loading: true, error: null });

  useEffect(() => {
    if (authLoading) return;
    if (!isSupabaseConfigured || !session) {
      setState({ data: null, loading: false, error: null });
      return;
    }

    let cancelled = false;
    setState((s) => ({ ...s, loading: true }));

    fetcher().then(({ data, error }) => {
      if (cancelled) return;
      setState({ data: data ?? null, loading: false, error: error?.message ?? null });
    });

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [session, authLoading, ...deps]);

  return state;
}

export function useTodayCache(): QueryState<DailyCache> {
  const today = new Date().toISOString().slice(0, 10);
  return useLumiQuery<DailyCache>(
    () =>
      supabase
        .from("daily_cache")
        .select("*")
        .eq("user_id", CURRENT_USER_ID)
        .eq("cache_date", today)
        .maybeSingle(),
    [today],
  );
}

export function useNatalChart(): QueryState<NatalChart> {
  return useLumiQuery<NatalChart>(
    () =>
      supabase
        .from("natal_chart")
        .select("*")
        .eq("user_id", CURRENT_USER_ID)
        .order("updated_at", { ascending: false })
        .limit(1)
        .maybeSingle(),
    [],
  );
}

export function useAppSettings(): QueryState<AppSetting[]> {
  return useLumiQuery<AppSetting[]>(
    () => supabase.from("app_settings").select("*").eq("user_id", CURRENT_USER_ID).then((r) => ({ data: r.data, error: r.error })),
    [],
  );
}

export function useAgentSessions(limit = 10): QueryState<AgentSession[]> {
  return useLumiQuery<AgentSession[]>(
    () =>
      supabase
        .from("agent_sessions")
        .select("*")
        .eq("user_id", CURRENT_USER_ID)
        .order("updated_at", { ascending: false })
        .limit(limit)
        .then((r) => ({ data: r.data, error: r.error })),
    [limit],
  );
}
