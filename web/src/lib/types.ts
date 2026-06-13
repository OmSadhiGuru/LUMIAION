// Mirrors the public schema of the LUMIAION Supabase project.
// Keep in sync with any migrations applied to project lwwrfcdvgxnynetjmnmx.

export interface NatalChart {
  id: number;
  user_id: string;
  birth_date: string;
  birth_time: string | null;
  birth_location: string;
  latitude: number | null;
  longitude: number | null;
  sun_sign: string | null;
  moon_sign: string | null;
  rising_sign: string | null;
  sun_lon: number | null;
  moon_lon: number | null;
  mercury_lon: number | null;
  venus_lon: number | null;
  mars_lon: number | null;
  jupiter_lon: number | null;
  saturn_lon: number | null;
  uranus_lon: number | null;
  neptune_lon: number | null;
  pluto_lon: number | null;
  north_node_lon: number | null;
  chiron_lon: number | null;
  ascendant_lon: number | null;
  mc_lon: number | null;
  mercury_sign: string | null;
  venus_sign: string | null;
  mars_sign: string | null;
  jupiter_sign: string | null;
  saturn_sign: string | null;
  uranus_sign: string | null;
  neptune_sign: string | null;
  pluto_sign: string | null;
  north_node_sign: string | null;
  chiron_sign: string | null;
  aspects: unknown[];
  houses: Record<string, unknown>;
  chart_data: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export interface DailyCache {
  id: number;
  user_id: string;
  cache_date: string;
  journal_entries: unknown[];
  journal_count: number;
  goals_snapshot: unknown[];
  goals_completed: number;
  goals_active: number;
  fitness_log: Record<string, unknown>;
  fitness_readiness: number | null;
  finance_log: Record<string, unknown>;
  essence_snapshot: Record<string, unknown>;
  moon_phase: string | null;
  hq_snapshot: Record<string, unknown>;
  neural_events_count: number;
  agent_activity: Record<string, unknown>;
  synced_to_supabase: boolean;
  synced_to_notion: boolean;
  notion_page_id: string | null;
  supabase_sync_at: string | null;
  notion_sync_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface AppSetting {
  id: number;
  user_id: string;
  setting_key: string;
  setting_value: unknown;
  updated_at: string;
}

export interface AgentSession {
  id: number;
  user_id: string;
  session_date: string;
  agent_id: string;
  messages: ChatMessage[];
  nodes_activated: string[];
  edges_activated: string[];
  pulse_count: number;
  created_at: string;
  updated_at: string;
}

export interface SyncLog {
  id: number;
  user_id: string;
  sync_type: string;
  sync_target: string | null;
  records_synced: number;
  status: string | null;
  error_message: string | null;
  synced_at: string;
}

export interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
  model?: string;
  timestamp?: string;
}

export const CURRENT_USER_ID = "omsadhiguru";
