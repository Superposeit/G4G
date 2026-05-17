import SpaceMiniNav from "@/components/space/SpaceMiniNav";

export default function SpaceLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="flex h-full overflow-hidden">
      <div className="hidden md:block">
        <SpaceMiniNav />
      </div>
      <main className="flex-1 overflow-y-auto bg-[var(--background)] [scrollbar-gutter:stable]">
        <div className="mx-auto max-w-5xl px-4 py-5 pb-8 md:px-8 md:py-8 md:pb-12">
          {children}
        </div>
      </main>
    </div>
  );
}
