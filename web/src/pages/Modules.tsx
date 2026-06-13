import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { MODULES } from "../lib/modules";

export default function Modules() {
  return (
    <div className="pt-6 sm:pt-10">
      <h1 className="font-display text-2xl font-semibold sm:text-3xl">Every system, one brain</h1>
      <p className="mt-2 max-w-lg text-sm text-white/60">
        Each module is its own ode — its own fractal hue, its own purpose — but every one of them feeds back
        into the same consciousness.
      </p>

      <div className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2">
        {MODULES.map((mod, i) => (
          <motion.div
            key={mod.id}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.05 * i }}
          >
            <Link
              to={mod.path}
              className="glass group flex items-start gap-4 rounded-2xl p-5 transition hover:-translate-y-1"
              style={{ boxShadow: `0 0 0 1px ${mod.color}1a` }}
            >
              <div
                className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl"
                style={{ background: `${mod.color}22`, color: mod.color }}
              >
                <mod.icon size={22} />
              </div>
              <div>
                <div className="font-display text-base font-semibold">{mod.label}</div>
                <div className="mt-1 text-sm text-white/60">{mod.description}</div>
              </div>
            </Link>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
