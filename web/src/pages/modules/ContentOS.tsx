import ModuleHeader from "../../components/ModuleHeader";
import { SeedCard, EmptyState } from "../../components/Cards";
import { getModule } from "../../lib/modules";
import { Calendar, FileVideo, Lightbulb, Library } from "lucide-react";

const mod = getModule("content")!;

export default function ContentOS() {
  return (
    <div>
      <ModuleHeader module={mod} />

      <div className="mt-6 grid grid-cols-1 gap-3 sm:grid-cols-2">
        <SeedCard
          icon={Lightbulb}
          title="Idea bank"
          description="Every spark worth capturing, before it becomes content."
          color={mod.color}
        />
        <SeedCard
          icon={FileVideo}
          title="In production"
          description="Drafts, scripts and edits currently in motion."
          color={mod.color}
        />
        <SeedCard
          icon={Calendar}
          title="Publishing schedule"
          description="What goes out, where, and when."
          color={mod.color}
        />
        <SeedCard
          icon={Library}
          title="Creative archive"
          description="Everything you've shipped, organized and searchable."
          color={mod.color}
        />
      </div>

      <EmptyState
        title="Content OS tables coming next"
        description="Idea bank, production queue and the publishing calendar will get dedicated Supabase tables in a future pass."
      />
    </div>
  );
}
