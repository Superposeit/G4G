import { Suspense } from "react";
import MobileAppChrome from "@/components/mobile/MobileAppChrome";
import MobileChromeFallback from "@/components/mobile/MobileChromeFallback";
import WorkspaceSidebar from "@/components/sidebar/WorkspaceSidebar";
import { UnifiedChatProvider } from "@/context/UnifiedChatContext";
import { useAppShell } from "@/context/AppShellContext";
import { Menu } from "lucide-react";
import Image from "next/image";
import Link from "next/link";

function WorkspaceLayoutInner({ children }: { children: React.ReactNode }) {
  const { setMobileSidebarOpen } = useAppShell();
  return (
    <div className="flex h-screen flex-col overflow-hidden md:flex-row [height:100dvh]">
      {/* Mobile-only top header */}
      <header className="flex h-12 shrink-0 items-center gap-3 border-b border-[var(--border)]/40 bg-[var(--secondary)] px-4 md:hidden">
        <button
          onClick={() => setMobileSidebarOpen(true)}
          aria-label="Open sidebar"
          className="flex h-8 w-8 items-center justify-center rounded-lg text-[var(--muted-foreground)] transition-colors hover:bg-[var(--background)]/60 hover:text-[var(--foreground)]"
        >
          <Menu size={18} />
        </button>
        <Link href="/" className="flex items-center gap-2">
          <Image
            src="/logo-ver2.png"
            alt="DeepTutor"
            width={20}
            height={20}
            className="h-5 w-5 rounded-md"
          />
          <span className="text-[15px] font-semibold leading-none tracking-[-0.02em] text-[var(--foreground)]">
            DeepTutor
          </span>
        </Link>
      </header>

      {/* Sidebar (hidden on mobile via SidebarShell, drawer when open) */}
      <WorkspaceSidebar />

      <main className="flex-1 h-full overflow-hidden bg-[var(--background)]">
        {children}
      </main>
    </div>
  );
}

export default function WorkspaceLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <UnifiedChatProvider>
      <div className="relative flex h-[100dvh] overflow-hidden md:h-screen">
        <Suspense fallback={<MobileChromeFallback />}>
          <MobileAppChrome />
        </Suspense>
        <div className="hidden md:block">
          <WorkspaceSidebar />
        </div>
        <main className="mobile-app-shell-offset flex-1 overflow-hidden bg-[var(--background)] md:pt-0">
          {children}
        </main>
      </div>
    </UnifiedChatProvider>
  );
}
