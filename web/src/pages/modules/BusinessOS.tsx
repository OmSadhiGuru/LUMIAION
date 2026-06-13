import ModuleHeader from "../../components/ModuleHeader";
import { SeedCard, EmptyState } from "../../components/Cards";
import { getModule } from "../../lib/modules";
import { Briefcase, Handshake, Megaphone, Users } from "lucide-react";

const mod = getModule("business")!;

export default function BusinessOS() {
  return (
    <div>
      <ModuleHeader module={mod} />

      <div className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2">
        <SeedCard
          icon={Users}
          title="Clients"
          description="Every relationship, status and next step — the people you serve."
          color={mod.color}
        />
        <SeedCard
          icon={Briefcase}
          title="Products & services"
          description="What you offer, what it costs, and how it's delivered."
          color={mod.color}
        />
        <SeedCard
          icon={Megaphone}
          title="Leads"
          description="The pipeline — who's interested, where they are, and what's next."
          color={mod.color}
        />
        <SeedCard
          icon={Handshake}
          title="Coaching"
          description="Sessions, programs and the transformations you're guiding."
          color={mod.color}
        />
      </div>

      <EmptyState
        title="Business OS tables coming next"
        description="Clients, products, leads and coaching will get their own Supabase tables (with RLS) so this module comes alive with real data, just like Life OS and Agent OS."
      />
    </div>
  );
}
