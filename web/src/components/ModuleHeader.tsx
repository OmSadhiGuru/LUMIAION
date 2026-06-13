import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";
import type { ModuleDef } from "../lib/modules";

export default function ModuleHeader({ module }: { module: ModuleDef }) {
  return (
    <div className="pt-4 sm:pt-8">
      <Link to="/" className="inline-flex items-center gap-1 text-xs text-white/50 hover:text-white/80">
        <ArrowLeft size={14} /> Back to the brain
      </Link>

      <div className="mt-3 flex items-center gap-3">
        <div
          className="flex h-12 w-12 items-center justify-center rounded-2xl"
          style={{ background: `${module.color}22`, color: module.color }}
        >
          <module.icon size={24} />
        </div>
        <div>
          <h1 className="font-display text-2xl font-semibold sm:text-3xl">{module.label}</h1>
          <p className="text-sm text-white/50">{module.tagline}</p>
        </div>
      </div>

      <p className="mt-3 max-w-2xl text-sm text-white/60">{module.description}</p>
    </div>
  );
}
