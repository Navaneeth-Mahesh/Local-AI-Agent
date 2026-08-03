import { navigation } from "@/config/navigation";

export default function Sidebar() {
  return (
    <aside className="w-72 border-r">
      <div className="p-6 font-bold">
        AI Agent
      </div>

      <nav className="space-y-2 px-3">
        {navigation.map((item) => (
          <button
            key={item.href}
            className="flex w-full items-center gap-3 rounded-lg p-3 hover:bg-muted"
          >
            <item.icon size={18} />

            {item.label}
          </button>
        ))}
      </nav>
    </aside>
  );
}