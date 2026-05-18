export default function MobileChromeFallback() {
  return (
    <div
      aria-hidden
      className="fixed inset-x-0 top-0 z-40 border-b border-[var(--border)]/40 bg-[var(--secondary)]/92 backdrop-blur-md md:hidden"
      style={{ paddingTop: "env(safe-area-inset-top)" }}
    >
      <div className="h-14" />
    </div>
  );
}
