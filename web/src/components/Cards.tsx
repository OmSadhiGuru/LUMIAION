import type { ReactNode } from "react";
import type { LucideIcon } from "lucide-react";

export function StatCard({ label, value, hint }: { label: string; value: ReactNode; hint?: string }) {
  return (
    <div className="glass rounded-2xl px-4 py-3">
      <div className="text-xs uppercase tracking-wide text-white/40">{label}</div>
      <div className="mt-1 font-display text-lg font-semibold">{value}</div>
      {hint && <div className="mt-0.5 text-xs text-white/40">{hint}</div>}
    </div>
  );
}

export function SeedCard({
  icon: Icon,
  title,
  description,
  color,
}: {
  icon: LucideIcon;
  title: string;
  description: string;
  color: string;
}) {
  return (
    <div className="glass flex items-start gap-3 rounded-2xl p-4">
      <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl" style={{ background: `${color}22`, color }}>
        <Icon size={18} />
      </div>
      <div>
        <div className="font-display text-sm font-semibold">{title}</div>
        <div className="mt-0.5 text-xs text-white/55">{description}</div>
      </div>
    </div>
  );
}

export function EmptyState({ title, description }: { title: string; description: string }) {
  return (
    <div className="glass mt-6 rounded-2xl border border-dashed border-white/15 p-6 text-center">
      <div className="font-display text-sm font-semibold text-white/80">{title}</div>
      <p className="mx-auto mt-1 max-w-sm text-xs text-white/50">{description}</p>
    </div>
  );
}
