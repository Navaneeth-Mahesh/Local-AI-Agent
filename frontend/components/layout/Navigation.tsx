import {
  Bot,
  Brain,
  Database,
  Home,
  Settings,
  Wrench,
} from "lucide-react";

export const navigation = [
  {
    label: "Dashboard",
    href: "/dashboard",
    icon: Home,
  },
  {
    label: "Chat",
    href: "/chat",
    icon: Bot,
  },
  {
    label: "Knowledge",
    href: "/knowledge",
    icon: Database,
  },
  {
    label: "Memory",
    href: "/memory",
    icon: Brain,
  },
  {
    label: "Tools",
    href: "/tools",
    icon: Wrench,
  },
  {
    label: "Settings",
    href: "/settings",
    icon: Settings,
  },
];