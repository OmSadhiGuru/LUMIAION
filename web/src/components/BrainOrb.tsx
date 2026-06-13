import { motion } from "framer-motion";
import { MODULES } from "../lib/modules";

interface BrainOrbProps {
  /** 0-1 activity level per module id, e.g. { knowledge: 0.4, life: 0.7, ... } */
  activity?: Record<string, number>;
  size?: number;
}

const DEFAULT_ACTIVITY: Record<string, number> = {
  knowledge: 0.35,
  life: 0.5,
  business: 0.22,
  finance: 0.18,
  body: 0.3,
  content: 0.15,
  agents: 0.42,
};

/**
 * The central "brain" visualization: a pulsing core surrounded by one ring
 * per OS module, each glowing in proportion to its activity level.
 */
export default function BrainOrb({ activity, size = 260 }: BrainOrbProps) {
  const levels = { ...DEFAULT_ACTIVITY, ...activity };
  const center = size / 2;
  const ringGap = (size / 2 - 24) / MODULES.length;

  return (
    <div className="relative mx-auto" style={{ width: size, height: size }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} className="absolute inset-0">
        {MODULES.map((mod, i) => {
          const radius = 24 + ringGap * (i + 1);
          const level = Math.max(0.06, Math.min(1, levels[mod.id] ?? 0.1));
          const circumference = 2 * Math.PI * radius;
          return (
            <g key={mod.id}>
              <circle
                cx={center}
                cy={center}
                r={radius}
                fill="none"
                stroke="rgba(255,255,255,0.06)"
                strokeWidth={2}
              />
              <motion.circle
                cx={center}
                cy={center}
                r={radius}
                fill="none"
                stroke={mod.color}
                strokeWidth={3}
                strokeLinecap="round"
                strokeDasharray={circumference}
                initial={{ strokeDashoffset: circumference }}
                animate={{ strokeDashoffset: circumference * (1 - level) }}
                transition={{ duration: 1.4, ease: "easeOut", delay: i * 0.08 }}
                transform={`rotate(-90 ${center} ${center})`}
                style={{ filter: `drop-shadow(0 0 6px ${mod.color}aa)` }}
              />
            </g>
          );
        })}
      </svg>

      <motion.div
        className="absolute inset-0 flex items-center justify-center"
        animate={{ scale: [1, 1.05, 1] }}
        transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
      >
        <div
          className="flex h-20 w-20 items-center justify-center rounded-full font-display text-sm font-semibold uppercase tracking-widest text-white/90"
          style={{
            background: "radial-gradient(circle at 35% 30%, rgba(255,255,255,0.35), rgba(124,58,237,0.25))",
            boxShadow: "0 0 40px 12px rgba(124,58,237,0.45), inset 0 0 24px rgba(255,255,255,0.25)",
          }}
        >
          You
        </div>
      </motion.div>
    </div>
  );
}
