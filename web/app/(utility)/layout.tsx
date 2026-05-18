import { Suspense } from "react";
import MobileAppChrome from "@/components/mobile/MobileAppChrome";
import MobileChromeFallback from "@/components/mobile/MobileChromeFallback";
import UtilitySidebar from "@/components/sidebar/UtilitySidebar";

export default function UtilityLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="relative flex h-[100dvh] overflow-hidden md:h-screen">
      <Suspense fallback={<MobileChromeFallback />}>
        <MobileAppChrome />
      </Suspense>
      <div className="hidden md:block">
        <UtilitySidebar />
      </div>
      <main className="mobile-app-shell-offset flex-1 overflow-hidden bg-[var(--background)] md:pt-0">
        {children}
      </main>
    </div>
  );
}
