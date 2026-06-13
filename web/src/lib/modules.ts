import {
  BookOpen,
  Briefcase,
  Clapperboard,
  Dumbbell,
  LineChart,
  Network,
  Sparkles,
  type LucideIcon,
} from "lucide-react";

export interface ModuleDef {
  id: string;
  label: string;
  shortLabel: string;
  icon: LucideIcon;
  /** Hex accent color used for glows, gradients and the fractal tint on this module's page. */
  color: string;
  /** Hue (0-360) matching `color`, used to tint the fractal canvas. */
  hue: number;
  path: string;
  tagline: string;
  description: string;
}

export const MODULES: ModuleDef[] = [
  {
    id: "knowledge",
    label: "Knowledge Base",
    shortLabel: "Knowledge",
    icon: BookOpen,
    color: "#22d3ee",
    hue: 189,
    path: "/knowledge",
    tagline: "Everything you've learned, indexed",
    description:
      "Subjects, reading lists, goals and archives — the living library of everything you've studied, read and decided is worth remembering.",
  },
  {
    id: "life",
    label: "Life OS",
    shortLabel: "Life",
    icon: Sparkles,
    color: "#a78bfa",
    hue: 265,
    path: "/life",
    tagline: "Your natal chart, journal & essence",
    description:
      "Holistic personal development — your natal chart, daily journal, moon phases, and the inner essence that grounds every other system.",
  },
  {
    id: "business",
    label: "Business OS",
    shortLabel: "Business",
    icon: Briefcase,
    color: "#f5c542",
    hue: 45,
    path: "/business",
    tagline: "Clients, offers & coaching pipeline",
    description:
      "Clients, products, services, leads and coaching — the empire-building layer where ideas become offers and offers become income.",
  },
  {
    id: "finance",
    label: "Finance OS",
    shortLabel: "Finance",
    icon: LineChart,
    color: "#34d399",
    hue: 158,
    path: "/finance",
    tagline: "Vortex trading & wealth tracking",
    description:
      "The Vortex trading layer — wealth tracking, financial logs, and the numbers behind your freedom.",
  },
  {
    id: "body",
    label: "Body / Gym OS",
    shortLabel: "Body",
    icon: Dumbbell,
    color: "#fb7185",
    hue: 350,
    path: "/body",
    tagline: "Training, readiness & recovery",
    description:
      "Training logs, readiness scores and recovery — the temple maintenance layer that powers everything else.",
  },
  {
    id: "content",
    label: "Content OS",
    shortLabel: "Content",
    icon: Clapperboard,
    color: "#fb923c",
    hue: 25,
    path: "/content",
    tagline: "Creative pipeline & archive",
    description:
      "Your content creation pipeline — ideas, drafts, publishing schedule and the creative archive of everything you've made.",
  },
  {
    id: "agents",
    label: "Agent OS",
    shortLabel: "Agents",
    icon: Network,
    color: "#60a5fa",
    hue: 213,
    path: "/agents",
    tagline: "The AI hierarchy behind LUMIAION",
    description:
      "The hierarchy of AI agents that power LUMIAION — sessions, activated nodes and the neural pulse of the whole system.",
  },
];

export function getModule(id: string): ModuleDef | undefined {
  return MODULES.find((m) => m.id === id);
}
