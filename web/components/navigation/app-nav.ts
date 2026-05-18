import {
  BookOpen,
  Bot,
  LayoutGrid,
  Library,
  MessageSquare,
  PenLine,
  Settings,
  Sparkles,
  type LucideIcon,
} from "lucide-react";

export interface AppNavEntry {
  href: string;
  label: string;
  icon: LucideIcon;
  tooltipKey?: string;
}

export const PRIMARY_NAV: AppNavEntry[] = [
  {
    href: "/chat",
    label: "Chat",
    icon: MessageSquare,
    tooltipKey: "Chat tooltip",
  },
  {
    href: "/co-learn",
    label: "Co-Learn",
    icon: Sparkles,
    tooltipKey: "Co-Learn tooltip",
  },
  {
    href: "/agents",
    label: "TutorBot",
    icon: Bot,
    tooltipKey: "TutorBot tooltip",
  },
  {
    href: "/co-writer",
    label: "Co-Writer",
    icon: PenLine,
    tooltipKey: "Co-Writer tooltip",
  },
  {
    href: "/book",
    label: "Book",
    icon: Library,
    tooltipKey: "Book tooltip",
  },
  {
    href: "/knowledge",
    label: "Knowledge",
    icon: BookOpen,
    tooltipKey: "Knowledge tooltip",
  },
  {
    href: "/space",
    label: "Space",
    icon: LayoutGrid,
    tooltipKey: "Space tooltip",
  },
];

export const SECONDARY_NAV: AppNavEntry[] = [
  { href: "/settings", label: "Settings", icon: Settings },
];

export const GITHUB_REPO_URL = "https://github.com/HKUDS/DeepTutor";
export const BRAND_NAME = "EducaT TutorRD";
export const BRAND_LOGO_SRC = "/educat-tutorrd-logo-v3.svg";
