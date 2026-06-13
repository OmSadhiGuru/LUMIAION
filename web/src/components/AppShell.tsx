import { Link, Outlet, useLocation } from "react-router-dom";
import { Home, LayoutGrid, Settings } from "lucide-react";
import FractalCanvas from "./FractalCanvas";
import { MODULES, getModule } from "../lib/modules";
import { useMemo } from "react";

const HOME_HUE = 268;

export default function AppShell() {
  const location = useLocation();

  const activeModuleId = useMemo(() => {
    const match = MODULES.find((m) => location.pathname.startsWith(m.path));
    return match?.id;
  }, [location.pathname]);

  const hue = activeModuleId ? getModule(activeModuleId)?.hue ?? HOME_HUE : HOME_HUE;

  return (
    <div className="relative min-h-screen w-full overflow-hidden bg-void text-white">
      <div className="fixed inset-0">
        <FractalCanvas hue={hue} />
        <div className="absolute inset-0 bg-gradient-to-b from-void/35 via-void/55 to-void" />
      </div>

      <header className="safe-top sticky top-0 z-20 flex items-center justify-between px-4 py-3 sm:px-6">
        <Link to="/" className="flex items-center gap-2 font-display text-lg font-semibold tracking-wide">
          <span
            className="inline-block h-2.5 w-2.5 animate-pulse-slow rounded-full"
            style={{ background: `hsl(${hue}, 85%, 65%)`, boxShadow: `0 0 16px hsl(${hue}, 85%, 60%)` }}
          />
          LUMIAION
        </Link>
        <Link
          to="/settings"
          className="glass rounded-full p-2 text-white/70 transition hover:text-white"
          aria-label="Settings"
        >
          <Settings size={18} />
        </Link>
      </header>

      <main className="relative z-10 mx-auto w-full max-w-3xl px-4 pb-28 sm:px-6 lg:max-w-5xl xl:max-w-6xl">
        <Outlet />
      </main>

      <nav className="safe-bottom fixed inset-x-0 bottom-0 z-20 flex justify-center px-4 pb-3">
        <div className="glass flex w-full max-w-md items-center justify-around rounded-2xl px-2 py-2 shadow-2xl shadow-black/40">
          <NavLink to="/" icon={Home} label="Brain" active={location.pathname === "/"} />
          <NavLink to="/modules" icon={LayoutGrid} label="Modules" active={location.pathname === "/modules"} />
          <NavLink to="/settings" icon={Settings} label="Settings" active={location.pathname === "/settings"} />
        </div>
      </nav>
    </div>
  );
}

function NavLink({
  to,
  icon: Icon,
  label,
  active,
}: {
  to: string;
  icon: typeof Home;
  label: string;
  active: boolean;
}) {
  return (
    <Link
      to={to}
      className={`flex flex-1 flex-col items-center gap-1 rounded-xl py-2 text-xs transition ${
        active ? "text-white" : "text-white/50 hover:text-white/80"
      }`}
    >
      <Icon size={20} strokeWidth={active ? 2.4 : 2} />
      <span>{label}</span>
    </Link>
  );
}
